#!/bin/bash

python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --source_type "kaggle" \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_col_values 10 \
  --use_hint 1

python lc_nl2sql/predict/measure_example_generation_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/kaggle_example_generation_latency"
