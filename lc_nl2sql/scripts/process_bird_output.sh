#!/bin/bash

prefix="$1"
directory="$2"
multi_sql_mode="${3:-upper}"
n_cands="${4:--1}"          

if [ -z "$prefix" ] || [ -z "$directory" ]; then
  echo "Error: Please provide a prefix and directory path as arguments."
  exit 1
fi

if [[ "$prefix" == "cand" ]]; then
  python lc_nl2sql/eval/evaluation_bird.py \
        --sql_candidates_path "$directory" \
        --ground_truth_path lc_nl2sql/data/bird/dev/dev.sql \
        --db_root_path lc_nl2sql/data/bird/dev/dev_databases/ \
        --num_cpus 24 \
        --etype exec \
        --gt_tied_json_path lc_nl2sql/data/bird/dev/dev_tied_append.json \
        --diff_json_path lc_nl2sql/data/bird/dev/dev.json \
        --multi_sql_mode "$multi_sql_mode" \
        --n_cands "$n_cands"
else
  for pred_sql in "$directory"/"$prefix"*; do
    if [ -f "$pred_sql" ]; then
      echo "Processing file: $pred_sql"

      python lc_nl2sql/eval/evaluation_bird.py \
        --predicted_sql_path "$pred_sql" \
        --ground_truth_path lc_nl2sql/data/bird/dev/dev.sql \
        --db_root_path lc_nl2sql/data/bird/dev/dev_databases/ \
        --num_cpus 24 \
        --etype exec \
        --gt_tied_json_path lc_nl2sql/data/bird/dev/dev_tied_append.json \
        --diff_json_path lc_nl2sql/data/bird/dev/dev.json

    fi
done
fi

