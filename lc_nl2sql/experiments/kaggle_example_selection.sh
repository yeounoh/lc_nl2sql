#!/bin/bash

echo "Running with GT"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --source_type "kaggle" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --example_pool_type train \
  --example_selection_file lc_nl2sql/data/kaggle/similar_examples.json \
  --inject_gt_example 1 \
  --num_examples 1

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_example_selection_train_gt_0"


# Example selection experiments
n_examples=(5 20 50 75 100 125 200)
for k in "${n_examples[@]}"; do
  echo "Running with $k train examples"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --source_type "kaggle" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --example_pool_type train \
  --example_selection_file lc_nl2sql/data/kaggle/similar_examples.json \
  --num_examples "$k"

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_example_selection_train_$k"

  python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/kaggle_example_selection_train_$k" \
  --expected_num_examples $k


  echo "Running with $k train examples and GT"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --source_type "kaggle" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --example_pool_type train \
  --example_selection_file lc_nl2sql/data/kaggle/similar_examples.json \
  --inject_gt_example 1 \
  --num_examples "$k"

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_example_selection_train_gt_$k"


  echo "Running with $k dev examples"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --source_type "kaggle" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --example_pool_type dev \
  --example_selection_file lc_nl2sql/data/kaggle/similar_examples.json \
  --num_examples "$k"

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_example_selection_dev_$k"


  echo "Running with $k synthetic examples"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --source_type "kaggle" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --example_pool_type synthetic \
  --example_selection_file lc_nl2sql/data/kaggle/similar_examples.json \
  --num_examples "$k"

  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_example_selection_synthetic_$k"

done