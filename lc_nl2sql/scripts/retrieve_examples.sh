#!/bin/bash

# produce lc_nl2sql/data/bird/similar_examples.json
 python lc_nl2sql/data_process/retrieve_similar_examples.py \ 
 --project-id sysres-disagg-ml \
 --train-only-example-pool-path lc_nl2sql/data/train/train.json \ 
 --queries-path lc_nl2sql/data/bird/dev.json \
 --output-dir lc_nl2sql/data/bird \ 
 --synthetic-example-pool-path lc_nl2sql/data/bird/synthetic_examples.json
