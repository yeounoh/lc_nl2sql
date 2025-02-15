#!/bin/bash

echo "Use Beaver w/ gemini-1.5-pro"
input_file_sk100="lc_nl2sql/data/beaver_dev_example_synthetic_examples_100.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/beaver/queries.json \
  --input_table_path lc_nl2sql/data/beaver/tables.json \
  --output_file_path "$input_file_sk100" \
  --source_type "beaver" \
  --db_folder_path lc_nl2sql/data/beaver/databases \
  --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
  --num_col_values 10 \
  --synthetic_examples 1 \
  --use_column_filtering 1 \
  --filtered_schema_file lc_nl2sql/data/beaver/col_selection_schema.csv \
  --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/beaver/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/beaver_benchmark.sql"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename "$input_file_sk100" \
  --use_self_correction 0 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/beaver_measure_latency"
 

echo "Use Beaver w/ gemini-1.5-flash"
input_file_sk100="lc_nl2sql/data/beaver_dev_example_synthetic_examples_100_flash.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/beaver/queries.json \
  --input_table_path lc_nl2sql/data/beaver/tables.json \
  --output_file_path "$input_file_sk100" \
  --source_type "beaver" \
  --db_folder_path lc_nl2sql/data/beaver/databases \
  --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
  --filtered_schema_file lc_nl2sql/data/beaver/col_selection_schema.csv \
  --num_col_values 10 \
  --synthetic_examples 1 \
  --use_flash 1 \
  --use_column_filtering 1\
  --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --use_flash 1 \
  --db_folder_path lc_nl2sql/data/beaver/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/beaver_benchmark_flash.sql"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename "$input_file_sk100" \
  --use_self_correction 0 \
  --use_flash 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/beaver_measure_latency_flash"
