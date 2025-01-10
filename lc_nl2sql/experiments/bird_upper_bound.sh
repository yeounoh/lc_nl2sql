#!/bin/bash

python lc_nl2sql/process_and_predict.py \
        --input_data_path lc_nl2sql/data/bird/dev/dev.json \
        --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
        --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
        --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals.pickle \
        --temperature 1.8 \
        --use_column_filtering 1 \
        --num_examples 100 \
        --synthetic_examples 1 \
        --vertex_ai_project_id 400355794761 \
        --num_candidates 9

directory="output.csv"
multi_sql_mode="${3:-upper}"
n_cands=(1 3 5 7 9) 
for n in "${n_cands[@]}"; do
  python lc_nl2sql/eval/evaluation_bird.py \
        --sql_candidates_path "$directory" \
        --ground_truth_path lc_nl2sql/data/bird/dev/dev.sql \
        --db_root_path lc_nl2sql/data/bird/dev/dev_databases/ \
        --num_cpus 24 \
        --etype exec \
        --gt_tied_json_path lc_nl2sql/data/bird/dev/dev_tied_append.json \
        --diff_json_path lc_nl2sql/data/bird/dev/dev.json \
        --multi_sql_mode "upper" \
        --n_cands "$n"
done