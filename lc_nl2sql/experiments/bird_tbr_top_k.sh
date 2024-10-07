#!/bin/bash

# Use all the tables from DB
echo "Running with top_k = all tables from DB"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_tbr_top_all_tables" >> ${pred_log}

# Use simulated TBR with top_k and draw tables across the DBs.
k_values=(1 7 13 100) 
for k in "${k_values[@]}"; do
  echo "Running with top_k = $k"
  python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/bird/dev/dev.json \
    --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
    --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
    --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
    --extra_top_k "$k"

  python lc_nl2sql/predict/predict.py \
    --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
    --num_beams 1 \
    --temperature 0.5 \
    --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
    --predicted_out_filename "lc_nl2sql/output/pred/bird_tbr_top_$k" >> ${pred_log}


done