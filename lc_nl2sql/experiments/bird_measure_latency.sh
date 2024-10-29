#/bin/bash

echo "Small context..."
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 0 \
  --use_hint 1

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_small"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --use_flash 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_small_flash"

echo "Medium context..."
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 10 \
  --use_hint 1 

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_medium"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --use_flash 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_medium_flash"

echo "Large context..."
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 50 \
  --use_hint 1 

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_large"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --use_flash 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_large_flash"

echo "X-Large context..."
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 200 \
  --use_hint 1 

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_xlarge"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --use_flash 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_xlarge_flash"

echo "XX-Large context..."
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 500 \
  --use_hint 1 

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_xxlarge"

python lc_nl2sql/predict/measure_latency.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --use_flash 1 \
  --predicted_out_filename "lc_nl2sql/output/pred/latency/bird_measure_latency_xxlarge_flash"