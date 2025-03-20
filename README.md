# Long Context Evaluation for NL2SQL

We share the codes, artifacts and experiments for evaluating our long context LLM-based NL2SQL [arxiv](https://arxiv.org/abs/2501.12372). The original experiments were run using `gemini-1.5-pro` and `gemini-1.5-flash` -- via [Vertex AI](https://cloud.google.com/vertex-ai/docs/reference/rest). If you find this work, the experiments and insights useful, please cite (to appear at VLDB25)
```
@article{chung2025long,
  title={Is Long Context All You Need? Leveraging LLM's Extended Context for NL2SQL},
  author={Chung, Yeounoh and Kakkar, Gaurav T and Gan, Yu and Milne, Brenton and Ozcan, Fatma},
  journal={arXiv preprint arXiv:2501.12372},
  year={2025}
}
```

Some utility functions are taken from [DB-GPT-Hub](https://github.com/eosphoros-ai/DB-GPT-Hub) open source NL2SQL benchmark platform under MIT license.

All the experiments are packaged under `lc_nl2sql/experiments/` as individual shell script.

## Setup
The dependencies are tracked insdie `pyproject.toml`. We recommend `poetry` to manage the pakcages.
```
# at the root of the project
pip install poetry
poetry install
```

The full example generation relies on separate column selection results, we used the LLM-based approach from [CHESS](https://arxiv.org/abs/2405.16755). 
The example generation process in `sql_data_process.py` takes this optional parameter, 
```
--filtered_schema_file lc_nl2sql/data/bird/col_selection_schema.csv
```
The column selection results csv files for different benchmakrs are also provided under `lc_nl2sql/data/{benchmark}/`

For some table retrieval experiments require separate table retrieval results, some were directly dumped from our production pipelien. The example generation process in `sql_data_process.py` takes this optional parameter, 
```
--tbr_selection_file lc_nl2sql/data/bird/crs_dump.json \
```
The results are stored under `lc_nl2sql/data/bird/crs_dump.json` and `lc_nl2sql/data/kaggle/tbr_dump.json`.

We ran experiments for 4 different NL2SQL benchmarks (BIRD, SPIDER 1.0, KaggleDBQA, BEAVER). Running the experiments require setting `input_data_path` (required) `input_table_path` (required)`output_file_path` (required -- where to store the prepared dataset) `db_folder_path` (required) and other optional experiment specific parameters. 
we recommend installing/copying each benchamrk dataset under `lc_nl2sql/data/{benchmark}/` for convenience and compatibility with the existing experiment scripts and the paths.

For data preparation,
```
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
```

For inference/prediction,
```
python lc_nl2sql/predict/predict.py \
  --predicted_input_filename "$input_file_sk100" \
  --num_beams 10 \
  --temperature 0.5 \
  --use_self_correction 1 \
  --use_disambiguation 1 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_benchmark"
```

## Runnning the experiments
Run the experiment script as follows:
```
poetry bash lc_nl2sql/experiments/bird_benchmark.sh
```
The output and artifacts will be stored under `lc_nl2sql/output/pred/` or as specified in the experiment script (e.g., `--predicted_out_filename "lc_nl2sql/output/pred/bird_benchmark"`).
This also dumps some execution statistics (e.g., latency, n_retries) at the root (e.g., `stats_bird_benchmark.txt`)

## Evaluation
We have added evaluation scripts for different benchmarks. For instance,
```
poetry run bash lc_nl2sql/scripts/process_bird_output.sh bird_benchmark_flash lc_nl2sql/output/pred/
```
will output 
```
Processing file: lc_nl2sql/output/pred//bird_benchmark_flash
start calculate
                     simple               moderate             challenging          total               
count                925                  464                  145                  1534                
====================================== Exec Accuracy =====================================
accuracy             72.00                57.76                53.79                65.97               
===========================================================================================
Finished evaluation
```