
# Lost in the middle experiments
gt_pos=(0.1 0.25 0.5 0.75 0.9)
for k in "${gt_pos[@]}"; do
  echo "Running with $k train examples and GT"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --example_pool_type train \
  --example_selection_file lc_nl2sql/data/bird/similar_examples.json \
  --inject_gt_example 1 \
  --num_examples 100 \
  --gt_pos "$k"
  
  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_lost_in_the_middle_gt_pos_$k"
done

shuffle=(1 2 3)
for k in "${shuffle[@]}"; do
  echo "Running with shuffle mode $k"
  python lc_nl2sql/data_process/sql_data_process.py \
  --input_data_path lc_nl2sql/data/bird/dev/dev.json \
  --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --example_pool_type train \
  --example_selection_file lc_nl2sql/data/bird/similar_examples.json \
  --inject_gt_example 1 \
  --num_examples 100
  
  python lc_nl2sql/predict/predict.py \
  --predicted_input_filename lc_nl2sql/data/example_text2sql_dev.json \
  --num_beams 1 \
  --temperature 0.5 \
  --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
  --predicted_out_filename "lc_nl2sql/output/pred/bird_lost_in_the_middle_shuffle_$k"
done