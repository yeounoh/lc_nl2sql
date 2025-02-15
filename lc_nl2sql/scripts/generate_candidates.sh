#!/bin/bash
n_candidates="10"
python lc_nl2sql/process_and_predict.py \
        --output_file_path "lc_nl2sql/data/bird/bird_dev_candidates_$n_candidates.csv" \
        --input_data_path lc_nl2sql/data/bird/dev/dev.json \
        --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
        --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
        --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals.pickle \
        --temperature 1.8 \
        --vertex_ai_project_id 400355794761 \
        --num_candidates 10 \
        --reuse_data 0 \
        --shuffle_schema 2
        # --use_column_filtering 1 \
        # --num_examples 100 \
        # --synthetic_examples 1 \

python lc_nl2sql/process_and_predict.py \
        --output_file_path "lc_nl2sql/data/bird/bird_train_candidates_$n_candidates.csv" \
        --input_data_path lc_nl2sql/data/bird/train/train.json \
        --input_table_path lc_nl2sql/data/bird/train/train_tables.json \
        --db_folder_path lc_nl2sql/data/bird/train/train_databases \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals_train.pickle \
        --temperature 1.8 \
        --vertex_ai_project_id 400355794761 \
        --num_candidates 10 \
        --reuse_data 0 \
        --shuffle_schema 2
        # --use_column_filtering 1 \
        # --num_examples 100 \
        # --synthetic_examples 1 \
        
