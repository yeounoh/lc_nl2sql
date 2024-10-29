import os
import sys
import time
import numpy as np
import logging
import math

from lc_nl2sql.configs.config import EXAMPLE_GENERATOR, EXAMPLE_GENERATOR2

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from typing import List, Dict
from lc_nl2sql.llm_base.api_model import GeminiModel
from lc_nl2sql.predict.predict import prepare_dataset

def measure_example_generaitn_latency(model: GeminiModel, predict_data: List[Dict], n=100):
    def generate_k_examples(schema, k, diverse_set=True):
        num_generated_examples = 0
        examples = ""
        while num_generated_examples < k:
            _k = min(k - num_generated_examples, 128)
            if diverse_set:
                prompt = EXAMPLE_GENERATOR2.format(schema=schema, k=_k)
            else:
                prompt = EXAMPLE_GENERATOR.format(schema, _k)
            _examples = model._generate_sql(prompt)
            num_generated_examples += len(_examples.split("\"input\":"))
            examples += "\n" + _examples
        return examples
    
    latency = []
    for i, item in enumerate(predict_data):
        if i % 5 != 0:
            # Counting based on every other five questions
            continue
        schema = item["input"].split('###Table creation statements###'
            )[1].split('***************************')[0]
        
        start_time = time.time()
        generate_k_examples(schema, n//2, diverse_set=False)
        generate_k_examples(schema, n//2, diverse_set=True)
        latency.append(time.time() - start_time)
    return latency


def predict(model: GeminiModel, dump_file=True):
    args = model.data_args
    ## predict file can be give by param --predicted_input_filename ,output_file can be gived by param predicted_out_filename
    predict_data = prepare_dataset(args.predicted_input_filename)
    latency = measure_example_generaitn_latency(model, predict_data)
    avg_lat = np.mean(latency)
    std_lat = np.std(latency)

    if dump_file:
        with open(args.predicted_out_filename, "w") as f:
            f.write(str(avg_lat) + ", " + str(std_lat))
    else:
        return avg_lat, std_lat


if __name__ == "__main__":
    model = GeminiModel()
    model._infer_args()
    predict(model)
