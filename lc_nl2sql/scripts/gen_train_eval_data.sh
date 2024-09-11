# base spider dataset ,produce train and dev data
python dbgpt_hub/data_process/sql_data_process.py \
  --use_column_filtering 1 \
  --num_examples 50 \
  --synthetic_examples 1 \
  --filtered_schema_file dbgpt_hub/data/bird/col_selection_schema.csv \
  --input_data_path dbgpt_hub/data/bird/dev/dev.json \
  --input_table_path dbgpt_hub/data/bird/dev/dev_tables.json
