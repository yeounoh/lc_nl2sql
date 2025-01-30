#!/bin/bash

echo "BIRD mini ablation"
input_file_sk100="lc_nl2sql/data/mini_ablation_bird.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --output_file_path "$input_file_sk100" \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 10 \
  --use_hint 1 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 1 \
  --synthetic_examples 1 \
  --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_bird_no_diamb"

input_file_sk100="lc_nl2sql/data/mini_ablation_bird_no_synthetic.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --output_file_path "$input_file_sk100" \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 10 \
  --use_hint 1
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_bird_no_synthetic"


echo "Spider mini ablation"
input_file_sk100="lc_nl2sql/data/mini_ablation_spider.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/spider/test_data/dev.json \
    --input_table_path lc_nl2sql/data/spider/test_data/tables.json \
    --output_file_path "$input_file_sk100" \
    --source_type "spider" \
    --db_folder_path lc_nl2sql/data/spider/test_database \
    --db_tbl_col_vals_file db_tbl_col_vals_spider.pickle \
    --num_col_values 10 \
    --filtered_schema_file lc_nl2sql/data/spider/col_selection_schema_spider.csv \
    --use_column_filtering 1 \
    --synthetic_examples 1 \
    --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_spider.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/spider/test_database \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_spider_no_disamb.sql"

input_file_sk100="lc_nl2sql/data/mini_ablation_spider_no_synthetic.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/spider/test_data/dev.json \
    --input_table_path lc_nl2sql/data/spider/test_data/tables.json \
    --output_file_path "$input_file_sk100" \
    --source_type "spider" \
    --db_folder_path lc_nl2sql/data/spider/test_database \
    --db_tbl_col_vals_file db_tbl_col_vals_spider.pickle \
    --num_col_values 10
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_spider.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/spider/test_database \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_spider_no_synthetic.sql"


echo "Kaggle mini ablation"
input_file_sk100="lc_nl2sql/data/mini_ablation_kaggle.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/kaggle/dev.json \
    --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
    --output_file_path "$input_file_sk100" \
    --source_type "kaggle" \
    --db_folder_path lc_nl2sql/data/kaggle/databases \
    --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
    --num_col_values 10 \
    --use_column_filtering 1\
    --filtered_schema_file lc_nl2sql/data/kaggle/col_selection_schema.csv \
    --synthetic_examples 1 \
    --num_examples 200
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_kaggle_no_disamb.sql"

input_file_sk100="lc_nl2sql/data/mini_ablation_kaggle_no_synthetic.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/kaggle/dev.json \
    --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
    --output_file_path "$input_file_sk100" \
    --source_type "kaggle" \
    --db_folder_path lc_nl2sql/data/kaggle/databases \
    --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
    --num_col_values 10
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_kaggle_no_synthetic.sql"

echo "Beaver mini ablation"
input_file_sk100="lc_nl2sql/data/mini_ablation_beaver.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/beaver/queries.json \
    --input_table_path lc_nl2sql/data/beaver/tables.json \
    --output_file_path "$input_file_sk100" \
    --source_type "beaver" \
    --db_folder_path lc_nl2sql/data/beaver/databases \
    --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
    --num_col_values 10 \
    --synthetic_examples 1 \
    --use_column_filtering 1 \
    --filtered_schema_file lc_nl2sql/data/beaver/col_selection_schema.csv \
    --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/beaver/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_beaver_no_disamb.sql"

input_file_sk100="lc_nl2sql/data/mini_ablation_beaver_no_synthetic.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
    --input_data_path lc_nl2sql/data/beaver/queries.json \
    --input_table_path lc_nl2sql/data/beaver/tables.json \
    --output_file_path "$input_file_sk100" \
    --source_type "beaver" \
    --db_folder_path lc_nl2sql/data/beaver/databases \
    --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
    --num_col_values 10
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --db_tbl_col_vals_file db_tbl_col_vals_beaver.pickle \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/beaver/databases \
  --predicted_out_filename "lc_nl2sql/output/pred/mini_ablation_beaver_no_synthetic.sql"