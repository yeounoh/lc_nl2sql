#!/bin/bash

echo "Running with no error correction"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_self_correction_no_correction"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_self_correction_no_correction"


echo "Running with self-correction"
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --measure_self_correction_tokens 1 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_self_correction_self_correction" \
  --extra_token_measurement_filename "lc_nl2sql/output/pred/token_count/bird_self_correction_self_correction_extra"


echo "Runing with self-correction and entire schema and all column values for disambiguation"
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --measure_self_correction_tokens 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_self_correction_disambiguation" \
  --extra_token_measurement_filename "lc_nl2sql/output/pred/token_count/bird_self_correction_disambiguation_extra"


echo "Running with self-correction and LSH based column filtered schema"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_column_filtering_for_generation 1 \
  --use_self_correction 1 \
  --measure_self_correction_tokens 1 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_self_correction_filtered_columns" \
  --extra_token_measurement_filename "lc_nl2sql/output/pred/token_count/bird_self_correction_filtered_columns"



