#!/bin/bash

# Use different number of column values
n_col_values=(0 5 10 25 50 75 100)
for k in "${n_col_values[@]}"; do
  echo "Running with num_col_values = $k"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --num_col_values "$k"

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_num_col_vals_$k"

  python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_num_col_vals_$k"

done
