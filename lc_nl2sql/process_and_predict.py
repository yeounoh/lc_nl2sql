
import argparse
import os
import sys
import csv
import json

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

from lc_nl2sql.configs.config import DATA_PATH
from lc_nl2sql.data_process.data_utils import extract_sql_prompt_dataset
from lc_nl2sql.data_process.sql_data_process import ProcessSqlData
from lc_nl2sql.llm_base.api_model import GeminiModel
from lc_nl2sql.predict import predict

def main():
    parser = argparse.ArgumentParser()

    # Vertex AI project ID
    parser.add_argument("--vertex_ai_project_id", default="618488765595")

    # BIRD-Bench input files
    parser.add_argument("--input_data_path", default="")
    parser.add_argument("--input_table_path", default="")
    parser.add_argument("--db_folder_path", default="")
    parser.add_argument("--output_file_path", default="output.csv")

    # New flags
    parser.add_argument("--num_examples",
                        help="Retrieve relevant examples.",
                        default=0)
    parser.add_argument("--synthetic_examples", default=False)
    parser.add_argument(
        "--extra_top_k",
        help="Retrieve extra tables outside the DB to guarantee 'k' tables.",
        default=0)
    parser.add_argument("--column_description", default=True)
    parser.add_argument("--column_examples", default=True)
    parser.add_argument("--use_column_filtering", default=False)
    # filtered_schema_file dict (csv) from CHESS column selection
    # (selected_schema_with_connections);
    # column names: question_id,selected_schema_with_connections
    # this contains filtered database schema by question_id (key)
    parser.add_argument("--filtered_schema_file", default="")
    parser.add_argument("--db_tbl_col_vals_file", default="db_tbl_col_vals.pickle")

    parser.add_argument("--temperature", default=0.5)
    parser.add_argument("--num_candidates", default=10)

    args = parser.parse_args()

    all_in_one_dev_file = os.path.join(DATA_PATH, "example_text2sql_dev.json")
    process = ProcessSqlData(
        input_data_file=args.input_data_path,
        input_table_file=args.input_table_path,
        db_folder_path=args.db_folder_path,
        train_file="",
        dev_file=all_in_one_dev_file,
        extra_top_k=int(args.extra_top_k),
        num_examples=int(args.num_examples),
        synthetic_examples=bool(int(args.synthetic_examples)),
        column_description=bool(int(args.column_description)),
        column_examples=bool(int(args.column_examples)),
        use_column_filtering=bool(int(args.use_column_filtering)),
        filtered_schema_file=args.filtered_schema_file,
        db_tbl_col_vals_file=args.db_tbl_col_vals_file,
        vertex_ai_project_id=args.vertex_ai_project_id,
    )

    model = GeminiModel(project_id=args.vertex_ai_project_id)
    model._infer_args({"temperature": float(args.temperature),
                       "db_folder_path": args.db_folder_path,
                       "db_tbl_col_vals_file": args.db_tbl_col_vals_file})

    dev_data = process.create_sft_raw_data(dump_file=False)
    with open('lc_nl2sql/data/example_text2sql_dev.json', 'r') as f:
        dev_data = json.load(f)
    predict_data = [extract_sql_prompt_dataset(item) for item in dev_data]
    candidate_sets = list()
    candidate_sets.append([idx for idx in range(len(predict_data))])
    for i in range(int(args.num_candidates)):
        result = predict.parallelized_inference(model, predict_data)
        candidate_sets.append(result[0])
        with open(f'cand_{i}.txt', 'w') as f:
            for l in result[0]:
                f.write(l + "\n")
    with open(args.output_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(candidate_sets)

if __name__ == "__main__":
    main()
