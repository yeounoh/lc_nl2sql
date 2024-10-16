import os
import sys
import numpy as np
import logging
import math

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from typing import List, Dict
from lc_nl2sql.llm_base.api_model import GeminiModel
from lc_nl2sql.predict.predict import prepare_dataset

def count_token(model: GeminiModel, predict_data: List[Dict], sample=True):
    tok_cnts = []
    for i, item in enumerate(predict_data):
        if sample and i % 5 != 0:
            # Counting based on every other five questions
            continue
        num_examples = len(item['input'].split("###Examples")[1].split("\"input\":"))
        if num_examples == 1 and num_examples != model.data_args.expected_num_examples:
            num_examples = len(item['input'].split("###Examples")[1].split("\\\"input\\\":"))
        if (num_examples < math.floor(model.data_args.expected_num_examples * 0.93) or 
            num_examples > math.ceil(model.data_args.expected_num_examples * 1.07)):  # give some margin
            logging.error(f"Expected {model.data_args.expected_num_examples} but found {num_examples}")
        else:
            tok_cnts.append(model._count_token(item['input']))
    return tok_cnts


def predict(model: GeminiModel, dump_file=True):
    args = model.data_args
    ## predict file can be give by param --predicted_input_filename ,output_file can be gived by param predicted_out_filename
    predict_data = prepare_dataset(args.predicted_input_filename)
    tok_cnts = count_token(model, predict_data)
    avg_tok = np.mean(tok_cnts)
    std_tok = np.std(tok_cnts)

    if dump_file:
        with open(args.predicted_out_filename, "w") as f:
            f.write(str(avg_tok) + ", " + str(std_tok))
    else:
        return avg_tok, std_tok


if __name__ == "__main__":
    model = GeminiModel()
    model._infer_args()
    predict(model)
