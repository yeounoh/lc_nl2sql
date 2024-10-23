python lc_nl2sql/predict/predict.py \
    --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
    --num_beams 1 \
    --temperature 0.5 \
    --use_self_correction 1 \
    --use_disambiguation 1 \
    --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
    --predicted_out_filename lc_nl2sql/output/pred/pred_bird-gemini-pro-1.5-sql-lora.sql

