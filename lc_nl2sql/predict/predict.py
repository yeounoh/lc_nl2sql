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

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def prepare_dataset(predict_file_path: Optional[str] = None, ) -> List[Dict]:
    with open(predict_file_path, "r") as fp:
        data = json.load(fp)
    predict_data = [extract_sql_prompt_dataset(item) for item in data]
    return predict_data

def inference_worker(
        model, item, qid,
        input_kwargs):  # Worker function for a single inference task
    
    def validate_email(email):
                pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                return re.match(pattern, email) is not None
    
    def format_col_vals(tbl_col_vals):
        s = ""
        for tbl, col_vals in tbl_col_vals.items():
            for col, vals in col_vals.items():
                if len(vals) > 0 and validate_email(vals[0]):
                    continue
                if len(vals) > 50 and np.mean(
                    [len(v) for v in random.sample(vals, 10)]) > 90:
                    continue
                s += f'* `{tbl}`.`{col}`: [{",".join(vals[:])}]\n'
        return s
        
    def _task2():
        # verify and retry
        n_candidates = model.generating_args.num_beams     
        schema = item["input"].split('###Table creation statements###'
            )[1].split('***************************')[0]
        question = item["input"].split("###Question###"
                                       )[1].split('***************************')[0]
        cached_response = ""
        n_tries, extra_tokens = 0, 0
        for i in range(n_candidates):
            n_tries += 1
            model.set_temperature(model.generating_args.temperature + 0.1 * i)
            start_time = time.time()  # tracks output generation time
            response, _ = model.chat(query=item["input"],
                                     history=[],
                                     **input_kwargs)
            response, extra_tokens = model.verify_and_correct(item["input"], response,
                                                model.db_folder_path, qid, return_invalid=False)
            generation_latency = time.time() - start_time
            if response != "":
                cached_response = model.verify_answer(response, question, schema)
                if cached_response != "":
                    return cached_response, extra_tokens, n_tries, generation_latency
        model.set_temperature(model.generating_args.temperature)
        return cached_response, extra_tokens, n_tries, generation_latency
    try:
        return func_timeout(1800, _task2, args=())
    except FunctionTimedOut:
        return ("", 0)

def parallelized_inference(model: GeminiModel, predict_data: List[Dict],
                           **input_kwargs):
    num_threads = 50
    if model.generating_args.num_beams > 10:
        num_threads = 10

    res_dict = {}
    extra_tokens, n_tries, latency = [], [], []
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
                                            timeout=8000),
                               total=len(futures),
                               desc="Inference Progress",
                               unit="item"):
                index = futures[future]
                result = future.result()  # (sql, token_count)
                extra_tokens.append(result[1])
                n_tries.append(result[2])
                latency.append(result[3])
                res_dict[index] = result[0]
                if result[0] != "":
                    success_count += 1
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
    return [res_dict[i] for i in range(len(predict_data))], extra_tokens, n_tries, latency


def inference(model: GeminiModel, predict_data: List[Dict], **input_kwargs):
    res = []
    for item in tqdm(predict_data, desc="Inference Progress", unit="item"):
        n_candidates = 1
        cands = []
        for i in range(n_candidates):
            response, _ = model.chat(query=item["input"],
                                     history=[],
                                     **input_kwargs)
            response = model.verify_and_correct(item["input"], response,
                                                model.db_folder_path, i)
            cands.append(response)
        if n_candidates == 1:
            res.append(response)
        else:
            query = item["input"].split(
                'Also consider the "Rules" and some useful "Hints" if provided.'
            )[1].split(
                'Now generate SQLite SQL query to answer the given "Question".'
            )[0]
            res.append(model.majority_voting(query, cands))
    return res


def predict(model: GeminiModel, dump_file=True):
    args = model.data_args
    ## predict file can be give by param --predicted_input_filename ,output_file can be gived by param predicted_out_filename
    predict_data = prepare_dataset(args.predicted_input_filename)
    result, extra_tokens, n_tries, latency = parallelized_inference(model, predict_data)

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
        with open("stats.txt", 'w') as f:  
            try:
                tm, ts = np.mean(n_tries), np.std(n_tries)
            except:
                tm, ts = 0, 0
            try:
                lm, ls = np.mean(latency), np.std(latency)
            except:
                lm, ls = 0, 0
            f.write(f"avg(n_tries): {tm}, std(n_tries): {ts}, "
                    + f"avg(latency): {lm}, std(latency): {ls}")
    else:
        return result


if __name__ == "__main__":
    model = GeminiModel()
    model._infer_args()
    predict(model)
