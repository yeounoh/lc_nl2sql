import logging
import os
import json
import sys
import numpy as np
import time
import re
import random
import pickle

from func_timeout import func_timeout, FunctionTimedOut

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from tqdm import tqdm
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from lc_nl2sql.data_process.data_utils import extract_sql_prompt_dataset
from lc_nl2sql.llm_base.api_model import GeminiModel


def prepare_dataset(predict_file_path: Optional[str] = None, ) -> List[Dict]:
    with open(predict_file_path, "r") as fp:
        data = json.load(fp)
    predict_data = [extract_sql_prompt_dataset(item) for item in data]
    return predict_data

def extract_output(predict_file_path: Optional[str] = None, ) -> List[str]:
    with open(predict_file_path, "r") as fp:
        data = json.load(fp)
    output_sqls = [item['output'] for item in data]
    return output_sqls

def inference_worker(
        model, item, qid,
        input_kwargs):  # Worker function for a single inference task
        
    def _task2():
        # verify and retry
        n_candidates = model.generating_args.num_beams     
        schema = item["input"].split('###Table creation statements###'
            )[1].split('***************************')[0]
        question = item["input"].split("###Question###"
                                       )[1].split('***************************')[0]
        cached_response = ""
        n_tries, extra_tokens = 0, 0
        generation_latency, verification_latency = 0, 0
        e2e_latency = time.time()
        for i in range(n_candidates):
            model.set_temperature(model.generating_args.temperature + 0.1 * i)
            start_time = time.time()  # tracks output generation time
            response, _ = model.chat(query=item["input"],
                                     history=[],
                                     **input_kwargs)
            n_tries += 1
            response, extra_tokens, n_retries = model.verify_and_correct(item["input"], response,
                                                model.db_folder_path, qid, return_invalid=True, 
                                                use_flash=model.generating_args.use_flash)
            n_tries += n_retries
            generation_latency = time.time() - start_time
            if response != "":
                start_time = time.time()
                cached_response = model.verify_answer(response, question, schema, 
                                                      use_flash=model.generating_args.use_flash)
                verification_latency = time.time() - start_time
                if cached_response != "":
                    e2e_latency = time.time() - e2e_latency
                    return cached_response, extra_tokens, n_tries, generation_latency, verification_latency, e2e_latency
        model.set_temperature(model.generating_args.temperature)
        e2e_latency = time.time() - e2e_latency
        return cached_response, extra_tokens, n_tries, generation_latency, verification_latency, e2e_latency
    try:
        return func_timeout(1800, _task2, args=())
    except FunctionTimedOut:
        return ("", 0, 0, 0, 0, 0, 0)

def parallelized_inference(model: GeminiModel, predict_data: List[Dict],
                           **input_kwargs):
    num_threads = 50
    if model.generating_args.num_beams > 10:
        num_threads = 10

    res_dict = {}
    extra_tokens, n_tries, latency, verify_latency = [], [], [], []
    e2e_latency = []
    success_count, failure_count = 0, 0

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            executor.submit(inference_worker, model, item, i, input_kwargs): i
            for i, item in enumerate(predict_data)
        }
        n_total = len(futures)
        n_completed = 0
        try:
            for future in tqdm(as_completed(futures,
                                            timeout= 3600 * 3),
                               total=len(futures),
                               desc="Inference Progress",
                               unit="item"):
                index = futures[future]
                result = future.result()  # (sql, token_count)
                res_dict[index] = result[0]
                
                e2e_latency.append(result[5])

                if result[0] != "":
                    success_count += 1
                    if result[1] > 0:
                        extra_tokens.append(result[1])
                    if result[2] > 0:
                        n_tries.append(result[2])
                    if result[3] > 0:
                        latency.append(result[3])
                    if result[4] > 0:
                        verify_latency.append(result[4])
                else:
                    failure_count += 1
                n_completed = success_count + failure_count
                if n_completed == n_total:
                    executor.shutdown(wait=False)
                    break
                elif n_completed % 100 == 0:
                    logging.info(f"{n_total - n_completed} items remaining...")
        except TimeoutError as e:
            logging.info(e)
            executor.shutdown(wait=False)
    for i in range(len(predict_data)):
        if i not in res_dict:
            res_dict[i] = ""
            failure_count += 1
    logging.info(
        f"Successful inferences: {success_count}, Failed inferences: {failure_count}"
    )
    return [res_dict[i] for i in range(len(predict_data))], extra_tokens, n_tries, latency, verify_latency, e2e_latency


def predict(model: GeminiModel, dump_file=True):
    args = model.data_args
    ## predict file can be give by param --predicted_input_filename ,output_file can be gived by param predicted_out_filename
    predict_data = prepare_dataset(args.predicted_input_filename)
    result, extra_tokens, n_tries, latency, vlatency, e2e_latency = parallelized_inference(model, predict_data)

    if dump_file:
        with open(args.predicted_out_filename, "w") as f:
            for p in result:
                try:
                    f.write(p.replace("\n", " ") + "\n")
                except:
                    f.write("Invalid Output!\n")
        if model.measure_self_correction_tokens:
            with open(args.extra_token_measurement_filename, "w") as f:
                f.write(str(np.mean(extra_tokens)) + ", " + str(np.std(extra_tokens)))
        with open(f"stats_{args.predicted_out_filename.split('/')[-1]}.txt", 'w') as f:  
            def _compute_stats(vals):
                try:
                    m, s = np.mean(vals), np.std(vals)
                except:
                    m, s = 0, 0
                return m, s
            tm, ts = _compute_stats(n_tries)
            lm, ls = _compute_stats(latency)
            vlm, vls = _compute_stats(vlatency)
            elm, els = _compute_stats(e2e_latency)
            
            f.write(f"avg(n_tries): {tm}, std(n_tries): {ts}, "
                    + f"avg(latency): {lm}, std(latency): {ls}, "
                    + f"avg(vlatency): {vlm}, std(vlatency): {vls}"
                    + f"avg(e2e_latency): {elm}, std(e2e_latency): {els}")
    else:
        return result


if __name__ == "__main__":
    model = GeminiModel()
    model._infer_args()
    predict(model)
