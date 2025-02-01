#!/bin/bash

echo "Running with no error correction"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --source_type "kaggle" \
  --db_folder_path lc_nl2sql/data/kaggle/databases

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 0 \
  --use_disambiguation 0 \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_self_correction_no_correction"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/kaggle_self_correction_no_correction"


echo "Running with self-correction"
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --measure_self_correction_tokens 1 \
  --use_disambiguation 0 \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_self_correction_self_correction" \
  --extra_token_measurement_filename "lc_nl2sql/output/pred/token_count/kaggle_self_correction_self_correction_extra"


echo "Runing with self-correction and entire schema and all column values for disambiguation"
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --measure_self_correction_tokens 1 \
  --use_disambiguation 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_self_correction_disambiguation" \
  --extra_token_measurement_filename "lc_nl2sql/output/pred/token_count/kaggle_self_correction_disambiguation_extra"


echo "Running with self-correction and LSH based column filtered schema"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --source_type "kaggle" \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --filtered_schema_file lc_nl2sql/data/kaggle/col_selection_schema.csv

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --db_folder_path lc_nl2sql/data/kaggle/databases \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --measure_self_correction_tokens 1 \
  --use_column_filtering_for_correction 1 \
  --use_disambiguation 0 \
  --filtered_schema_file "lc_nl2sql/data/kaggle/col_selection_schema.csv" \
  --predicted_out_filename "lc_nl2sql/output/pred/kaggle_self_correction_filtered_columns" \
  --extra_token_measurement_filename "lc_nl2sql/output/pred/token_count/kaggle_self_correction_filtered_columns_extra"



