#!/bin/bash

prefix="$1"
directory="$2"

if [ -z "$prefix" ] || [ -z "$directory" ]; then
  echo "Error: Please provide a prefix and directory path as arguments."
  exit 1
fi

for pred_sql in "$directory"/"$prefix"*; do
  if [ -f "$pred_sql" ]; then
    echo "Processing file: $pred_sql"

    python lc_nl2sql/eval/evaluation.py \
      --input "$pred_sql" \
      --gold lc_nl2sql/data/spider/test_data/dev_gold.sql \
      --db lc_nl2sql/data/spider/test_database/ \
      --table lc_nl2sql/data/spider/test_data/tables.json \
      --etype exec
  fi
done

