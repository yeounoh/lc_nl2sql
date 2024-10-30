#!/bin/bash

echo "Use BIRD w/ gemini-1.5-flash"
input_file_sk100="lc_nl2sql/data/dev_example_synthetic_examples_100_flash.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --output_file_path "$input_file_sk100" \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 10 \
  --use_hint 1 \
  --use_flash 1 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 1 \
  --synthetic_examples 1 \
  --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --use_flash 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_benchmark_flash"

echo "Use BIRD w/ gemini-1.5-pro"
input_file_sk100="lc_nl2sql/data/dev_example_synthetic_examples_100.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --output_file_path "$input_file_sk100" \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 10 \
  --use_hint 1 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 1 \
  --synthetic_examples 1 \
  --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_benchmark"