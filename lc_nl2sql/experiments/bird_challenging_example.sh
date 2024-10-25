#!/bin/bash

echo "Running with all challenging examples"
python lc_nl2sql/data_process/sql_data_process.py \
--input_data_path lc_nl2sql/data/bird/dev/dev.json \
--input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
--output_file_path lc_nl2sql/data/dev_examples_challenging_example.json \
--db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
--challenging_example_only 1

python lc_nl2sql/predict/predict.py \
--predicted_input_filename lc_nl2sql/data/dev_examples_challenging_example.json \
--num_beams 1 \
--temperature 0.5 \
--db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
--predicted_out_filename "lc_nl2sql/output/pred/bird_challenging_example"

echo "Running with all challenging examples & synthetic"
python lc_nl2sql/data_process/sql_data_process.py \
--input_data_path lc_nl2sql/data/bird/dev/dev.json \
--input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
--output_file_path lc_nl2sql/data/dev_examples_challenging_synthetic_example.json \
--db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
--challenging_example_only 1 \
--example_pool_type synthetic \
--example_selection_file lc_nl2sql/data/bird/similar_examples.json \
--num_examples 50

python lc_nl2sql/predict/predict.py \
--predicted_input_filename lc_nl2sql/data/dev_examples_challenging_synthetic_example.json \
--num_beams 1 \
--temperature 0.5 \
--db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
--predicted_out_filename "lc_nl2sql/output/pred/bird_challenging_and_synthetic_example"