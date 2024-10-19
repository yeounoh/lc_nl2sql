#!/bin/bash

# Generate difference number of synthetic examples
n_examples=(5 10 25 50 100 200 500 1000)
for k in "${n_examples[@]}"; do
  echo "Running with $k synthetic examples"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 1 \
  --synthetic_examples 1 \
  --num_examples "$k"

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_synthetic_examples_$k"

  python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_synthetic_examples_$k" \
  --expected_num_examples $k

done
