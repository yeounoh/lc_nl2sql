#!/bin/bash

# Example selection experiments
n_examples=(5 25 75 125)
for k in "${n_examples[@]}"; do
  output_file="lc_nl2sql/data/dev_example_with_codes_examples_$k.json"
  if [[ ! -f "$output_file" ]]; then
    python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/bird/dev/dev.json \
    --output_file_path "$output_file" \
    --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
    --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
    --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
    --use_column_filtering 1 \
    --synthetic_examples 1 \
    --use_codes 1 \
    --num_examples "$k"
  fi

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$output_file" \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_codes_examples_$k"
done
