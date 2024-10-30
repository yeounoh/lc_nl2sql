#!/bin/bash

echo "Use Spider w/ gemini-1.5-pro"
input_file_sk100="lc_nl2sql/data/spider_dev_example_synthetic_examples_100.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/spider/test_data/dev.json \
  --input_table_path lc_nl2sql/data/spider/test_data/   qtables.json \
  --output_file_path "$input_file_sk100" \
  --db_folder_path lc_nl2sql/data/spider/test_database \
  --num_col_values 10 \
  --filtered_schema_file lc_nl2sql/data/spider/col_selection_schema_spider.csv \
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
  --db_folder_path lc_nl2sql/data/spider/test_database \
  --predicted_out_filename "lc_nl2sql/output/pred/spider_benchmark"

echo "Use Spider w/ gemini-1.5-flash"
input_file_sk100="lc_nl2sql/data/spider_dev_example_synthetic_examples_100.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/spider/test_data/dev.json \
  --input_table_path lc_nl2sql/data/spider/test_data/   qtables.json \
  --output_file_path "$input_file_sk100" \
  --db_folder_path lc_nl2sql/data/spider/test_database \
  --num_col_values 10 \
  --use_flash 1 \
  --filtered_schema_file lc_nl2sql/data/spider/col_selection_schema_spider.csv \
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
  --db_folder_path lc_nl2sql/data/spider/test_database \
  --predicted_out_filename "lc_nl2sql/output/pred/spider_benchmark_flash"

