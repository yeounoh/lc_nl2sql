import logging
import os
import json
import sys
import numpy as np
import time
import random

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


from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def inference_worker(
        model, item, qid,
        input_kwargs):  # Worker function for a single inference task

    def _task():
        n_candidates = model.generating_args.num_beams
        n_repeat = 3 if n_candidates > 1 else 1
        cands = []
        for i in range(n_candidates):
            response, _ = model.chat(query=item["input"],
                                     history=[],
                                     **input_kwargs)
            response, extra_tokens = model.verify_and_correct(item["input"], response,
                                                model.db_folder_path, qid)
            cands.append(response)
            time.sleep(random.randint(1,3))
        if n_candidates == 1:
            return (response, extra_tokens)
        else:
            query = item["input"].split(
                '- If the hints provide a mathematical computation, make sure you closely follow the mathematical compuation.'
            )[1].split(
                'Now generate SQLite SQL query to answer the given "Question".'
            )[0]
            new_cands = list()
            for i in range(n_repeat):
                new_cands.append(model.majority_voting(query, cands))
                time.sleep(random.randint(1,3))
            return (model.majority_voting(query, new_cands), 0)

    try:
        return func_timeout(600, _task, args=())
    except FunctionTimedOut:
        return ("", 0)

def parallelized_inference(model: GeminiModel, predict_data: List[Dict],
                           **input_kwargs):
    num_threads = 50 if model.generating_args.num_beams < 3 else 20
    if model.generating_args.num_beams > 10:
        num_threads = 10

    res_dict = {}
    extra_tokens = []
    success_count, failure_count = 0, 0

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            executor.submit(inference_worker, model, item, i, input_kwargs): i
            for i, item in enumerate(predict_data)
        }
        n_total = len(futures)
        try:
            for future in tqdm(as_completed(futures,
                                            timeout=8000),
                               total=len(futures),
                               desc="Inference Progress",
                               unit="item"):
                index = futures[future]
                result = future.result()  # (sql, token_count)
                extra_tokens.append(result[1])
                res_dict[index] = result[0]
                if result[0] != "":
                    success_count += 1
                else:
                    failure_count += 1
                if (success_count + failure_count) == n_total:
                    executor.shutdown(wait=False)
                    break
        except TimeoutError as e:
            logging.info(e)
            for i in range(len(predict_data)):
                if i not in res_dict:
                    res_dict[i] = ""
                    failure_count += 1
            executor.shutdown(wait=False)
    logging.info(
        f"Successful inferences: {success_count}, Failed inferences: {failure_count}"
    )
    return [res_dict[i] for i in range(len(predict_data))], extra_tokens


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
    result, extra_tokens = parallelized_inference(model, predict_data)

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
    else:
        return result


if __name__ == "__main__":
    model = GeminiModel()
    model._infer_args()
    predict(model)
