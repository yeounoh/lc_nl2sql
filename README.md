# Long Context Evaluation for NL2SQL

The work here done to Google Gemini long context models.
Some utility functions and file structures are taken from DB-GPT-Hub open source project under MIT license.

The data generation relies on CHESS column selection result,
that can be referenced in `gen_train_eval_data.sh` (or `sql_data_process.py`) all:
```
--filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv
```

At a high-level, there are two key components,
- `llm_base/api_model.py` SQL generation & agentic workflows
- `data_process/sql_data_process.py` data preprocessing & example generation

## Generating answer candidates
### Dumping all candidates into a csv file
It is recommended to install the package
```
python setup.py sdist bdist_wheel
pip install dist/lc_nl2sql-0.1.1-py3-none-any.whl
```
and run the following to generate the candidates into a csv file.
```
lc_nl2sql \
    --input_data_path {path_to_input_data_file/dev.json} \
    --input_table_path {path_to_input_table_file/dev_tables.json} \
    --db_folder_path {path_to_input_db_folder/dev_databases} \
    --filtered_schema_file {path_to_filtered_schema_file/col_selection_schema.csv} \
    --db_tbl_col_vals_file {path_to_column_value_cache/db_tbl_col_vals.pickle} \
    --temperature 0.5 \
    --use_column_filtering 1 \
    --num_examples 50 \
    --synthetic_examples 1 \
    --num_candidates 10 \
    --output_file_path {path_to_output_file/output.csv}
```

Alternatively, you can poetry the script:
```
poetry run sh scripts/generate_candidates_new.sh
```

### Dumping each candidate set into a sql file
`scripts/generate_candidates.sh` calls the data proprocessing and SQL generation commands.
```
poetry run sh scripts/generate_candidates.sh
```
You can modify the output filename, number of candidates to generate.
Modify `--temperature 0.5` to a desired value.
