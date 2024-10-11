#!/bin/bash

prefix="$1"
directory="$2"

if [ -z "$prefix" ] || [ -z "$directory" ]; then
  echo "Error: Please provide a prefix and directory path as arguments."
  exit 1
fi

for pred_sql in "$directory"/"$prefix"*; do
  if [ -f "$pred_sql" ]; then
    echo "Processing file: $pred_sql (display: mean, std)"
    cat $pred_sql
    echo ""

  fi
done