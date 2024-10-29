import os
import sys
import numpy as np
import logging
import math

from lc_nl2sql.configs.config import VERIFY_ANSWER

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from typing import List, Dict
from lc_nl2sql.llm_base.api_model import GeminiModel
from lc_nl2sql.predict.predict import prepare_dataset, extract_output

def count_token(model: GeminiModel, predict_data: List[Dict], output_sqls: List[str], sample=True):
    tok_cnts = []
    for i, item in enumerate(predict_data):
        if sample and i % 5 != 0:
            # Counting based on every other five questions
            continue
        schema = item["input"].split('###Table creation statements###'
            )[1].split('***************************')[0]
        question = item["input"].split("###Question###"
                                       )[1].split('***************************')[0]
        sql = output_sqls[i]
        prompt = VERIFY_ANSWER.format(sql=sql, question=question, schema=schema)
        tok_cnts.append(model._count_token(prompt))
    return tok_cnts


def predict(model: GeminiModel, dump_file=True):
    args = model.data_args
    ## predict file can be give by param --predicted_input_filename ,output_file can be gived by param predicted_out_filename
    predict_data = prepare_dataset(args.predicted_input_filename)
    output_sqls = extract_output(args.predicted_input_filename)
    tok_cnts = count_token(model, predict_data, output_sqls)
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
