import os
import sys
import time
import numpy as np
import logging
import math

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from lc_nl2sql.configs.config import EXAMPLE_GENERATOR, EXAMPLE_GENERATOR2

from typing import List, Dict
from lc_nl2sql.llm_base.api_model import GeminiModel
from lc_nl2sql.predict.predict import prepare_dataset

def measure_latency(model: GeminiModel, predict_data: List[Dict], n=100, use_flash=False):
    toks, latency = [], []
    for i, item in enumerate(predict_data):
        if i % 15 != 0:
            # Counting based on every other 15 samples
            continue
        try:
            tok = model._count_token(item["input"])
            start_time = time.time()
            # measure single request latency
            _, _ = model.chat(query=item["input"], history=[], use_flash=use_flash)
            latency.append(time.time() - start_time)
            toks.append(tok)
        except:
            continue
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
