#!/bin/bash

counter=1
while [ $counter -le 10 ]; do
        echo "iteration $counter"
        # path to the generated set of answer candidates
        out_file="/root/candidates/cand_${counter}.sql"
        echo $out_file

        python dbgpt_hub/data_process/sql_data_process.py \
        --use_column_filtering 1 \
        --num_examples 50 \
        --synthetic_examples 1 \
        --filtered_schema_file dbgpt_hub/data/bird/col_selection_schema.csv \
        --db_tbl_col_vals_file dbgpt_hub/data/bird/db_tbl_col_vals.pickle \
        --db_folder_path dbgpt_hub/data/bird/dev/dev_databases \
        --input_data_path dbgpt_hub/data/bird/dev/dev.json \
        --input_table_path dbgpt_hub/data/bird/dev/dev_tables.json

        CUDA_VISIBLE_DEVICES=0 python dbgpt_hub/predict/predict.py \
        --predicted_input_filename dbgpt_hub/data/example_text2sql_dev.json \
        --predicted_out_filename "$out_file" \
        --num_beams 1 \
        --temperature 0.5 \
        --db_tbl_col_vals_file dbgpt_hub/data/bird/db_tbl_col_vals.pickle \
        --db_folder_path dbgpt_hub/data/bird/dev/dev_databases
        counter=$((counter + 1))
done
