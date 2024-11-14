#!/bin/bash

# Using train dataset
num_candidates=5
python lc_nl2sql/process_and_predict.py \
        --vertex_ai_project_id 400355794761 \
        --input_data_path lc_nl2sql/data/bird/train/train.json \
        --input_table_path lc_nl2sql/data/bird/train/train_tables.json \
        --output_file_path "lc_nl2sql/data/train_candidates_$num_candidates.csv" \
        --db_folder_path lc_nl2sql/data/bird/train/train_databases \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/train_db_tbl_col_vals.pickle \
        --temperature 0.5 \
        --num_candidates "$num_candidates"

python lc_nl2sql/eval/label_bird.py \
        --ground_truth_path lc_nl2sql/data/bird/train/train_gold.sql \
        --db_root_path lc_nl2sql/data/bird/train/train_databases/ \
        --gt_tied_json_path "" \
        --sql_candidates_path "lc_nl2sql/data/train_candidates_${num_candidates}.csv" \
        --sql_candidates_with_label_path "lc_nl2sql/data/train_candidates_${num_candidates}_label.csv"


# Using dev dataset
# python lc_nl2sql/process_and_predict.py \
#         --input_data_path lc_nl2sql/data/bird/dev/dev.json \
#         --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
#         --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
#         --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
#         --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals.pickle \
#         --temperature 0.5 \
#         --use_column_filtering 1 \
#         --num_examples 50 \
#         --synthetic_examples 1 \
#         --num_candidates 10
