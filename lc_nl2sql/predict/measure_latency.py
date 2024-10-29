import os
import sys
import time
import numpy as np
import logging
import math

from tqdm import tqdm
from func_timeout import func_timeout, FunctionTimedOut
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from lc_nl2sql.configs.config import EXAMPLE_GENERATOR, EXAMPLE_GENERATOR2

from typing import List, Dict
from lc_nl2sql.llm_base.api_model import GeminiModel
from lc_nl2sql.predict.predict import prepare_dataset


def measure(
        model, item):  # Worker function for a single inference task
        
    def _task():
        try:
            token = model._count_token(item["input"])
            start_time = time.time()
            # measure single request latency
            _, _ = model.chat(query=item["input"], history=[], use_flash=use_flash)
            latency = time.time() - start_time
            return latency, token
        except:
            return 0, 0
    try:
        return func_timeout(300, _task, args=())
    except FunctionTimedOut:
        return 0, 0

def measure_latency(model: GeminiModel, predict_data: List[Dict], n=100, use_flash=False):
    
    toks, latency = [], []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {
            executor.submit(measure, model, item): i
            for i, item in enumerate(predict_data) if i % 15 == 0
        }

        try:
            for future in tqdm(as_completed(futures,
                                            timeout=1200),
                               total=len(futures),
                               desc="Measure latency Progress",
                               unit="item"):
                index = futures[future]
                result = future.result()  # (sql, token_count)
                
                if result[0] > 0:
                    latency.append(result[0])
                if result[1] > 0:
                    toks.append(result[1])
        except TimeoutError as e:
            logging.info(e)
            executor.shutdown(wait=False)
    return toks, latency


def predict(model: GeminiModel):
    args = model.data_args
    ## predict file can be give by param --predicted_input_filename ,output_file can be gived by param predicted_out_filename
    predict_data = prepare_dataset(args.predicted_input_filename)
    toks, latency = measure_latency(model, predict_data, n=100, 
                                    use_flash=model.generating_args.use_flash)

    with open(args.predicted_out_filename, "w") as f:
        for t, l in zip(toks, latency):
            f.write(str(t) + ", " + str(l) + "\n")


if __name__ == "__main__":
    model = GeminiModel()
    model._infer_args()
    predict(model)
