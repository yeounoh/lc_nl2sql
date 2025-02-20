counter=1
while [ $counter -le 10 ]; do
        echo "iteration $counter"
        # path to the generated set of answer candidates
        out_file="/root/candidates/cand_dev_${counter}.sql"
        echo $out_file

        inp_file="lc_nl2sql/data/cand_gen_input.json"
        python lc_nl2sql/data_process/sql_data_process.py \
        --output_file_path "$inp_file" \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals.pickle \
        --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
        --input_data_path lc_nl2sql/data/bird/dev/dev.json \
        --input_table_path lc_nl2sql/data/bird/dev/dev_tables.json \
        --shuffle_schema 2

        python lc_nl2sql/predict/predict.py \
        --predicted_input_filename "$inp_file" \
        --predicted_out_filename "$out_file" \
        --num_beams 1 \
        --use_self_correction 1 \
        --use_disambiguation 1 \
        --temperature 1.8 \
        --db_folder_path lc_nl2sql/data/bird/dev/dev_databases \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals.pickle

        out_file="/root/candidates/cand_train_${counter}.sql"
        echo $out_file

        inp_file="lc_nl2sql/data/cand_gen_input.json"
        python lc_nl2sql/data_process/sql_data_process.py \
        --output_file_path "$inp_file" \
        --input_data_path lc_nl2sql/data/bird/train/train.json \
        --input_table_path lc_nl2sql/data/bird/train/train_tables.json \
        --db_folder_path lc_nl2sql/data/bird/train/train_databases \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals_train.pickle \
        --shuffle_schema 2

        python lc_nl2sql/predict/predict.py \
        --predicted_input_filename "$inp_file" \
        --predicted_out_filename "$out_file" \
        --num_beams 1 \
        --use_self_correction 1 \
        --use_disambiguation 1 \
        --temperature 1.8 \
        --db_folder_path lc_nl2sql/data/bird/train/train_databases \
        --db_tbl_col_vals_file lc_nl2sql/data/bird/db_tbl_col_vals_train.pickle

        counter=$((counter + 1))
done