#!/bin/bash

echo "Use Kaggle w/ gemini-1.5-pro"
input_file_sk100="lc_nl2sql/data/kaggle_dev_example_synthetic_examples_200.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --output_file_path "$input_file_sk100" \
  --source_type "kaggle" \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_col_values 10 \
  --synthetic_examples 1 \
  --num_examples 100
  #--filtered_schema_file lc_nl2sql/data/kaggle/col_selection_schema_kaggle.csv \
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_benchmark.sql"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename "$input_file_sk100" \
  --use_self_correction 0 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/kaggle_measure_latency"
 

echo "Use Kaggle w/ gemini-1.5-flash"
input_file_sk100="lc_nl2sql/data/kaggle_dev_example_synthetic_examples_200_flash.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --output_file_path "$input_file_sk100" \
  --source_type "kaggle" \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_col_values 10 \
  --synthetic_examples 1 \
  --use_flash 1 \
  --num_examples 100
  #--filtered_schema_file lc_nl2sql/data/kaggle/col_selection_schema_kaggle.csv \
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --use_flash 1 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_benchmark_flash.sql"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename "$input_file_sk100" \
  --use_self_correction 0 \
  --use_flash 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/kaggle_measure_latency_flash"
