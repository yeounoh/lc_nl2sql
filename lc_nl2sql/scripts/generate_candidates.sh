#!/bin/bash

python lc_nl2sql/process_and_predict.py \
        --input_data_path lc_nl2sql/data/bird/dev/dev.json \
        --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
        --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
        --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals.pickle \
        --temperature 0.5 \
        --use_column_filtering 1 \
        --num_examples 50 \
        --synthetic_examples 1 \
        --num_candidates 10
