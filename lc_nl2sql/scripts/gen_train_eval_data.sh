# base spider dataset ,produce train and dev data
python lc_nl2sql/data_process/sql_data_process.py \
  --use_column_filtering 1 \
  --num_examples 50 \
  --synthetic_examples 1 \
  --filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases
