#!/bin/bash

counter=1
while [ $counter -le 12 ]; do
        echo "iteration $counter"
        # path to the generated set of answer candidates
        out_file="/root/candidates/cand_${counter}.sql"
        echo $out_file

        inp_file="lc_nl2sql/data/dev_example_with_synthetic_examples_100.json"
        # python lc_nl2sql/data_process/sql_data_process.py \
        # --use_column_filtering 1 \
        # --num_examples 100 \
        # --synthetic_examples 1 \
        # --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
        # --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals.pickle \
        # --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
        # --input_data_path lc_nl2sql/data/bird/dev/dev.json \
        # --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json

        python lc_nl2sql/predict/predict.py \
        --predicted_input_filename "$inp_file" \
        --predicted_out_filename "$out_file" \
        --num_beams 1 \
        --use_self_correction 1 \
        --use_disambiguation 1 \
        --temperature 0.5 \
        --db_folder_path lc_nl2sql/data/bird/dev/dev_databases
        counter=$((counter + 1))
done
