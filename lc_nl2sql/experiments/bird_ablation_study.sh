#!/bin/bash

# Baseline piepeline for other experiments
# 1. Use all tables from DB
# 2. Use hint & rules
# 3. Use self correction 
# 4. 50 col vals

# ablation baseline, add in the folloiwng order
# - all talbes from DB (x -- TODO no self correction, no distinct col vals, no hint, no rules) 
# - rules  (x -- TODO no self correction, no distinct col vals, no hint) 
# - hint (x -- TODO no self correction, no distinct col vals)
# - add distinct column values (o -- no self correction run)
# - self correction (o -- with self correciton run)
#---------------------------------- (eval baseline)
# - add examples (o -- 100 examples)
# - expensive disambiguation (x -- with examples)
# - multiple choice / selection (x)

# Complete piepeline
# 1. Use all tables from DB
# 2. Use hint and rules
# 3. Use 50 (distinct) col vals
# 4. Use self correction 
# 5. Use expensive disambiguation (all dictinct values (str))
# 6. Use 100 synthetic examples (<32k vs. >32k)
# 8. multiple choice and select
echo "Ablation 1. Use all tables from DB"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 0 \
  --use_hint 0 \
  --use_rules 0 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 1 \
  --synthetic_examples 1 \
  --num_examples 0

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 0 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_ablation_1_all_tables"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_1_all_tables"

echo "Ablation 2. + hint"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 0 \
  --use_hint 1 \
  --use_rules 0 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 0 \
  --synthetic_examples 0 \
  --num_examples 0

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 0 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_ablation_2_hint"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_2_hint"

echo "Ablation 3. + distinct column values"
python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 10 \
  --use_hint 1 \
  --use_rules 0 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 0 \
  --synthetic_examples 0 \
  --num_examples 0

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 0 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_ablation_3_col_values"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_3_col_values"

# echo "Ablation 4. + self correction"
# share the data from 3
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 0 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_ablation_4_self_correction"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_4_self_correction"

echo "Ablation 5. + disambiguation"
# share the data from 3 & 4.
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_ablation_5_disambiguation"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_5_disambiguation"

echo "Ablation 6. + synthetic examples"
input_file_sk100="lc_nl2sql/data/dev_example_synthetic_examples_100.json"
if [[ ! -f "$input_file_sk100" ]]; then
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --output_file_path "$input_file_sk100" \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
  --num_col_values 10 \
  --use_hint 1 \
  --use_rules 0 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --use_column_filtering 1 \
  --synthetic_examples 1 \
  --num_examples 100
fi

python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --num_beams 1 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_ablation_6_synthetic_examples"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename "$input_file_sk100" \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_6_synthetic_examples"


echo "Ablation 7. + verify & retry"
# share the data from 6.
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_ablation_7_verify_retry"

python lc_nl2sql/predict/count_token.py \
  --predicted_input_filename "$input_file_sk100" \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_7_verify_retry"

python lc_nl2sql/predict/count_verify_token.py \
  --predicted_input_filename "$input_file_sk100" \
  --predicted_out_filename "lc_nl2sql/output/pred/token_count/bird_ablation_7_verify_retry_verify"