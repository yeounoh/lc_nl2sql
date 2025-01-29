#/bin/bash

echo "Small context..."
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/kaggle/dev.json \
  --input_table_path lc_nl2sql/data/kaggle/KaggleDBQA_tables.json \
  --db_tbl_col_vals_file db_tbl_col_vals_kaggle.pickle \
  --source_type "kaggle" \
  --db_folder_path lc_nl2sql/data/kaggle/databases

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --use_self_correction 0 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/kaggle_measure_latency_small"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --use_flash 1 \
  --use_self_correction 0 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/kaggle_measure_latency_small_flash"
