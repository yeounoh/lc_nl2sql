from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import os
import pandas as pd
import json
import sqlite3
import sys
import re
import argparse
import random
import pickle
import numpy as np
from tqdm import tqdm
import pandas as pd

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from lc_nl2sql.configs.config import (BASIC_INSTRUCTION_PROMPT,
                                      BASIC_INSTRUCTION_PROMPT_NO_RULES,
                                      EXAMPLE_GENERATOR, SQL_DATA_INFO,
                                      DATA_PATH, EXAMPLE_GENERATOR2,
                                      COLUMN_SELECTOR_TEMPLATE)
from lc_nl2sql.llm_base.api_model import GeminiModel


class ProcessSqlData:

    def __init__(
        self,
        input_data_file,
        input_table_file,
        db_folder_path,
        train_file=None,
        dev_file=None,
        extra_top_k=0,
        num_examples=0,
        synthetic_examples=False,
        column_description=False,
        column_examples=False,
        use_column_filtering=False,
        num_col_values=50,
        filtered_schema_file="",
        db_tbl_col_vals_file="",
        vertex_ai_project_id="",
        tbr_selection_file="",
        use_hint=True,
        use_rules=True,
        example_pool_type="train",
        example_selection_file="",
        inject_gt_example=False,
        document_pool_type="long",
        document_selection_file="",
        num_documents=0,
    ) -> None:
        self.input_data_file = input_data_file
        self.input_table_file = input_table_file
        self.db_folder_path = db_folder_path
        self.train_file = train_file
        self.dev_file = dev_file
        self.extra_top_k = extra_top_k
        self.num_examples = num_examples
        self.synthetic_examples = synthetic_examples
        self.column_description = column_description
        self.column_examples = column_examples
        self.use_column_filtering = use_column_filtering
        self.num_col_values = num_col_values
        self.filtered_schema_file = filtered_schema_file
        self.db_tbl_col_vals_file = db_tbl_col_vals_file
        self.tbr_selection_file = tbr_selection_file
        self.use_hint = use_hint
        self.use_rules = use_rules
        self.example_pool_type = example_pool_type
        self.example_selection_file = example_selection_file
        self.inject_gt_example = inject_gt_example
        self.document_pool_type = document_pool_type
        self.document_selection_file = document_selection_file
        self.num_documents = num_documents

        self.emb_model = None
        self.model = GeminiModel(vertex_ai_project_id)

    def decode_json_file_with_ddl(self, data_file_list, table_file,
                                  db_folder_path, db_id_name, output_name,
                                  col_selected_schemas):

        if table_file.endswith(".json"):
            all_tables = json.load(open(table_file))
            datas = []
            for data_file in data_file_list:
                datas.extend(json.load(open(data_file)))
            for i, data in enumerate(datas):
                if 'question_id' not in data:
                    data['question_id'] = i
                if i not in col_selected_schemas:
                    col_selected_schemas[i] = ""
                elif (not col_selected_schemas[i]
                        or str(col_selected_schemas[i]) == 'nan'):
                    col_selected_schemas[i] = ""
        else:
            logging.error("Unsupported file types")
            raise

        # Simulated TBR result. If not present, we do a static retrieval
        # over available DB tables.
        qid_tbr = dict()
        if self.tbr_selection_file:
            with open(self.tbr_selection_file, 'r') as file:
                tbr_selection = json.load(file)
            for i, v in enumerate(tbr_selection):
                qid = int(v['question_id'])
                qid_tbr[qid] = [t.split('/')[-1] for t in v['response_tables']]

        # Example selection result file by question similarity (Gecko)
        if os.path.exists(self.example_selection_file):
            with open(self.example_selection_file, 'r') as f:
                # ['sql_prompt', 'sql']
                similar_examples = json.load(f)

        # Document selection result file by question-content similarity (Gecko)
        if os.path.exists(self.document_selection_file):
            with open(self.document_selection_file, 'r') as f:
                similar_documents = pd.read_json(f)

        def truncate_example(val):
            s = str(val)
            if len(s) > 100:
                return s[:100] + f'...[{len(s) - 100} truncated]'
            else:
                return s

        def _process_table_schema(item):
            db_path = os.path.join(db_folder_path,
                                   item['db_id']) + f"/{item['db_id']}.sqlite"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            tables = item['table_names_original']
            columns = item['column_names_original'][1:]
            column_descs = item['column_names'][1:]
            column_types = item['column_types'][1:]
            column_examples = [list() for _ in range(len(columns))]
            primary_key = item["primary_keys"]
            foreign_keys = item["foreign_keys"]

            tbl_col_vals = {}
            for i, table in enumerate(tables):
                tbl_col_vals[table] = {}
                for j, col in enumerate(columns):
                    if col[0] == i:
                        tbl_col_vals[table][col[1]] = list()
                        example_vals = list()
                        try:
                            nval_limit = 5

                            extend_text_examples = True
                            if extend_text_examples:
                                sql = (
                                    f"SELECT typeof(`{col[1]}`) FROM `{table}`"
                                )
                                rows = cursor.execute(sql).fetchall()
                                col_type = rows[0][0].lower() if len(
                                    rows) > 0 else ""

                                if "text" in col_type:
                                    sql = (
                                        f"SELECT count(DISTINCT `{col[1]}`) "
                                        f" FROM `{table}` WHERE `{col[1]}` IS NOT NULL"
                                    )
                                    sql = f"SELECT count(*) FROM `{table}`"

                                    def validate_email(email):
                                        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                                        return re.match(pattern,
                                                        email) is not None

                                    too_many_col_vals = (
                                        'time' in col[1].lower()
                                        or 'phone' in col[1].lower()
                                        or 'date' in col[1].lower()
                                        or '_id' in col[1].lower()
                                        or 'url' in col[1].lower()
                                        or 'uuid' in col[1].lower())
                                    if not too_many_col_vals:
                                        nval_limit = self.num_col_values
                                        sql = (
                                            f'SELECT DISTINCT `{col[1]}` FROM `{table}` WHERE'
                                            f' `{col[1]}` IS NOT NULL')
                                        rows = cursor.execute(sql).fetchall()

                                        if (len(rows) > 0
                                                and validate_email(rows[0][0])
                                            ) or (len(rows) > 50 and np.mean([
                                                len(r) for r in random.sample(
                                                    rows, 10)
                                            ]) > 95):
                                            nval_limit = 5
                                        else:
                                            tbl_col_vals[
                                                table][col[1]] = [
                                                    ','.join(
                                                        map(
                                                            truncate_example,
                                                            r)).replace(
                                                                '\n', ',')
                                                    for r in rows
                                                ]

                            sql = (
                                f'SELECT DISTINCT `{col[1]}` FROM `{table}` WHERE'
                                f' `{col[1]}` IS NOT NULL LIMIT {nval_limit}')
                            rows = cursor.execute(sql).fetchall()
                            example_vals = [
                                ','.join(map(truncate_example,
                                             r)).replace('\n', ',')
                                for r in rows
                            ]
                        except sqlite3.Error as e:
                            logging.info(
                                f"Failed to retrieve example values for {col[1]} due to {e}"
                            )
                        column_examples[j] = example_vals

            table_schema_map = dict()
            table_creation_statements = ""
            for i, name in enumerate(tables):
                ddl_statements = [f'CREATE TABLE `{name}` (\n']
                for j, col in enumerate(columns):
                    if col[0] == i:
                        is_primary_key = False
                        for key in primary_key:
                            if type(key) == int:
                                is_primary_key = key == (j + 1)
                            elif type(key) == list:
                                is_primary_key = (j + 1) in key
                            else:
                                logging.info(
                                    f"Invalid primary key format from the table definition: {primary_key[i]}"
                                )
                        fk_str = ""
                        if not is_primary_key:
                            for key_pair in foreign_keys:
                                if key_pair[0] == (j + 1):
                                    fk_str = (
                                        f"\n    foreign key ({columns[j][1]}) "
                                        f"references {tables[columns[key_pair[1] - 1][0]]} ({columns[key_pair[1] - 1][1]})"
                                    )
                        col_name = col[1]
                        col_type = column_types[j]
                        col_comment = ""
                        if self.column_description:
                            col_comment = column_descs[j][1]
                        if self.column_examples:
                            if column_examples[j]:
                                col_comment += f" Example values: {column_examples[j]}"
                        col_key = "\n    primary key" if is_primary_key else ""
                        col_key += fk_str
                        ddl_statements.append(
                            f'  `{col_name}` {col_type}{col_key}, -- {col_comment} \n'
                        )
                ddl_statements.append(");\n")
                table_creation_statements += "".join(ddl_statements)
                if name not in table_schema_map:
                    table_schema_map[name] = ddl_statements
            return tbl_col_vals, table_creation_statements, table_schema_map

        n_workers = 40

        # store comprehensive table column value examples
        db_tbl_col_vals = dict()
        db_table_schema_map = dict()
        db_context = dict()

        # Load cached contents
        try:
            if os.path.exists(f'db_context_ncv{self.num_col_values}.cache'):
                with open(f'db_context_ncv{self.num_col_values}.cache', 'rb') as file:
                    db_context = pickle.load(file)
            if os.path.exists(f'db_table_schema_map_ncv{self.num_col_values}.cache'):
                with open(f'db_table_schema_map_ncv{self.num_col_values}.cache', 'rb') as file:
                    db_table_schema_map = pickle.load(file)
            if os.path.exists(self.db_tbl_col_vals_file):
                with open(self.db_tbl_col_vals_file, "rb") as file:
                    db_tbl_col_vals = pickle.load(file)
        except:
            db_tbl_col_vals = dict()
            db_table_schema_map = dict()
            db_context = dict()

        if len(db_tbl_col_vals) == 0 or len(db_table_schema_map) == 0 and len(db_context) == 0:
            with ThreadPoolExecutor(max_workers=n_workers) as executor:
                futures = {
                    executor.submit(_process_table_schema, item): item['db_id']
                    for item in all_tables
                }
                try:
                    for future in tqdm(as_completed(futures),
                                    total=len(futures),
                                    desc="Processing table schemas",
                                    unit="item"):
                        tbl_col_vals, table_creation_statements, table_schema_map = future.result()
                        db_tbl_col_vals[futures[future]] = tbl_col_vals
                        db_context[futures[future]] = table_creation_statements
                        db_table_schema_map[futures[future]] = table_schema_map
                except TimeoutError as e:
                    logging.error(e)
                    raise

            # Caching for faster experimentation.
            with open(f'db_context_ncv{self.num_col_values}.cache', 'wb') as file:
                pickle.dump(db_context, file)
            with open(f'db_table_schema_map_ncv{self.num_col_values}.cache', 'wb') as file:
                pickle.dump(db_table_schema_map, file)
            # Extra bookeeping for text example values.
            # This is used later for literal error fix.
            with open(self.db_tbl_col_vals_file, "wb") as file:
                pickle.dump(db_tbl_col_vals, file)

        def extract_k_tables(db_context, target_db_id, k, tbr_result=[]):
            # retrieve k tables for random
            create_stmts = db_context[target_db_id].split(";")
            if len(tbr_result) > 0:
                # retrieve k tables based on the simulation result
                retrieved_table_stmts = set()
                for retrieved_tbl_name in tbr_result[:k]:
                    for stmt in create_stmts:
                        if retrieved_tbl_name in stmt.split('(')[0]:
                            retrieved_table_stmts.add(stmt)
                create_stmts = list(retrieved_table_stmts)
            else:
                create_stmts = create_stmts[:k]

            # add extra tables from other DBs
            extra_table_cnt = k - len(create_stmts)
            while extra_table_cnt > 0:
                for key, val in db_context.items():
                    if extra_table_cnt <= 0:
                        break
                    if key == target_db_id:
                        continue
                    _stmts = val.split(";")
                    for s in _stmts:
                        if extra_table_cnt > 0:
                            create_stmts.append(s)
                            extra_table_cnt -= 1
                        else:
                            break
            return ";".join(create_stmts)

        def select_table_columns(schema, question, hint):
            prompt = COLUMN_SELECTOR_TEMPLATE.format(DATABASE_SCHEMA=schema,
                                                     QUESTION=question,
                                                     HINT=hint)
            return self.model._generate_sql(prompt)

        def generate_k_examples(schema, k, diverse_set=True):
            num_generated_examples = 0
            examples = ""
            while num_generated_examples < k:
                _k = min(k - num_generated_examples, 128)
                if diverse_set:
                    prompt = EXAMPLE_GENERATOR2.format(schema=schema, k=_k)
                else:
                    prompt = EXAMPLE_GENERATOR.format(schema, _k)
                _examples = self.model._generate_sql(prompt)
                num_generated_examples += len(_examples.split("\"input\":"))
                examples += "\n" + _examples
            return examples
            

        def filter_tables(table_schema_map, filtered_col_json):
            tables = []
            for item in json.loads(filtered_col_json.replace("json ", "")):
                tname = item.split(":")[0]
                if tname:
                    tables = table_schema_map.get(tname, "")
            return "".join(tables)

        def _generate_examples(db_id_key):
            schema = db_context[db_id_key]
            examples = ""
            if self.num_examples > 0 and self.synthetic_examples:
                examples = generate_k_examples(schema,
                            self.num_examples // 2 + self.num_examples % 2)
                if not self.use_column_filtering:
                    examples += "\n" + generate_k_examples(
                        schema, self.num_examples // 2, diverse_set=False)
            return examples

        db_examples = dict()
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = {
                executor.submit(_generate_examples, db_id_key): db_id_key
                for db_id_key in db_context.keys()
            }
            try:
                for future in tqdm(as_completed(futures),
                                   total=len(futures),
                                   desc="Generate examples",
                                   unit="item"):
                    db_examples[futures[future]] = future.result()
            except TimeoutError as e:
                logging.error(e)
                for k in db_context.keys():
                    if k not in db_examples:
                        db_examples[k] = ""
                executor.shutdown()

        def _filter_schema(schema):
            filtered_schema =""
            if len(col_selected_schemas) > 0:
                filtered_schema = col_selected_schemas[int(
                    data['question_id'])]
            if not filtered_schema:
                filtered_col_json = select_table_columns(
                    schema, data['question'], data['evidence'])
                table_schema_map = db_table_schema_map[
                    data[db_id_name]]
                filtered_schema = filter_tables(
                    table_schema_map, filtered_col_json)
            return filtered_schema
        
        def _extract_k_documents(qid, k):
            docs = similar_documents.iloc[qid]
            if self.document_pool_type == 'long':
                selected_docs = docs['long_knn'][:k]  
            elif self.document_pool_type == 'short':
                selected_docs = docs['short_knn'][:k]
            else:
                raise
            k_documents = ""
            for d in selected_docs:
                k_documents += d['doc'] + '\n\n'
            return k_documents

        def _context_packing(data):
            if data[db_id_name] in db_context.keys():
                # all tables and columns with primary and foreign keys.
                schema = db_context[data[db_id_name]]
                if self.extra_top_k > 0:
                    schema = extract_k_tables(db_context, data[db_id_name],
                                              self.extra_top_k,
                                              qid_tbr[int(data['question_id'])] if int(data['question_id']) in qid_tbr else []
                                              )
                if self.use_column_filtering:
                    filtered_schema = _filter_schema(schema)

                examples = ""
                if self.num_examples > 0:
                    if self.synthetic_examples:
                        examples = db_examples[data[db_id_name]]
                        if self.use_column_filtering:
                            examples += "\n" + generate_k_examples(
                                filtered_schema,
                                self.num_examples // 2,
                                diverse_set=False)
                    else:
                        assert os.path.exists(self.example_selection_file)
                        qid = int(data['question_id'])
                        if self.example_pool_type == 'train':
                            selected_examples = similar_examples[qid]['selected_train_only_examples']
                        elif self.example_pool_type == 'dev':
                            selected_examples = similar_examples[qid]['selected_dev_only_examples']
                        elif self.example_pool_type == 'synthetic':
                            selected_examples = similar_examples[qid]['selected_synthetic_only_examples']
                        elif self.example_pool_type == 'train_synthetic':
                            selected_examples = similar_examples[qid]['selected_train_and_synthetic_examples']
                        else:
                            raise
                        
                        shot_template = r"""
                        \"input\": \"{sql_prompt}\"\n
                        \"output\": \"{sql}\"\n
                        """
                        selected_examples = selected_examples[:self.num_examples]
                        shots = list()
                        for i, eg in enumerate(selected_examples):
                            if i == len(selected_examples)//2 and self.inject_gt_example:
                                shots.append(shot_template.format(sql_prompt=data["question"], sql=data['SQL']))
                            shots.append(shot_template.format(
                                sql_prompt=eg['sql_prompt'], 
                                sql=eg['sql']))
                        examples += '\n'.join(shots)

                documentation = ""
                if self.num_documents > 0:
                    documentation = _extract_k_documents(int(data['question_id']), self.num_documents)

                hints = data["evidence"] if "evidence" in data and self.use_hint else ""
                if self.use_rules:
                    input_instruction = BASIC_INSTRUCTION_PROMPT.format(
                        db_name=data[db_id_name],
                        hints=hints,
                        schema= schema,
                        examples=examples,
                        documentation=documentation,
                        question=data["question"])
                else:
                    input_instruction = BASIC_INSTRUCTION_PROMPT_NO_RULES.format(
                        db_name=data[db_id_name],
                        hints=hints,
                        schema= schema,
                        examples=examples,
                        documentation=documentation,
                        question=data["question"])

                input_idx = input_instruction.find("###Question###")
                input = {
                    "db_id": data[db_id_name],
                    "instruction": input_instruction[:input_idx],
                    "input": input_instruction[input_idx:],
                    "output": data[output_name],
                    "history": [],
                }
                return input

        res_dict = {}
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = {
                executor.submit(_context_packing, item): i
                for i, item in enumerate(datas)
            }
            try:
                for future in tqdm(as_completed(futures),
                                   total=len(futures),
                                   desc="Context packing",
                                   unit="item"):
                    index = futures[future]
                    result = future.result()
                    res_dict[index] = result
            except TimeoutError as e:
                logging.error(e)
                for i in range(len(datas)):
                    if i not in res_dict:
                        res_dict[i] = ""
                executor.shutdown()

        # dump examples
        if False:
            example_list = list()
            for i in range(len(datas)):
                qid = i
                estr = res_dict[i]["instruction"].split("###Examples###")[
                    1].split("***************************")[0]
                example_list.append({"question_id": qid, "examples": estr})
            with open("examples.json", 'w') as f:
                json.dump(example_list, f, indent=4)

        res = [res_dict[i] for i in range(len(datas))]
        return res

    def create_sft_raw_data(self, dump_file=True):
        dev_data = []
        for data_info in SQL_DATA_INFO:
            if data_info['data_source'] in ['bird', 'spider']:
                col_selected_schemas = dict()
                if (self.use_column_filtering) and self.filtered_schema_file:
                    df = pd.read_csv(self.filtered_schema_file)
                    id_name, schema_name = 'question_id', 'selected_schema_with_connections'
                    col_selected_schemas = dict()
                    for k, v in zip(df[id_name], df[schema_name]):
                        col_selected_schemas[int(k)] = v
                dev_data.extend(
                    self.decode_json_file_with_ddl(
                        data_file_list=[self.input_data_file],
                        table_file=self.input_table_file,
                        db_folder_path=self.db_folder_path,
                        db_id_name=data_info["db_id_name"],
                        output_name=data_info["output_name"],
                        col_selected_schemas=col_selected_schemas,
                    ))
                if dump_file:
                    with open(self.dev_file, "w", encoding="utf-8") as s:
                        json.dump(dev_data, s, indent=4, ensure_ascii=False)
                return dev_data
            else:
                logging.error("non BIRD-Bench dataset is not supported.")
                raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_data_path")
    parser.add_argument("--input_table_path")
    parser.add_argument("--db_folder_path")

    parser.add_argument("--column_description", default=True)
    parser.add_argument("--column_examples", default=True)
    parser.add_argument("--num_col_values", default=50)
    
    parser.add_argument("--num_examples",
                        help="Retrieve relevant examples.",
                        default=0)
    # Synthetic example generation
    parser.add_argument("--synthetic_examples", default=False)
    parser.add_argument("--use_column_filtering", default=False)  # for example generation
    # Example selection
    # - example_pool_type: train, dev, synthetic
    parser.add_argument("--example_pool_type", default='train')
    parser.add_argument("--example_selection_file", default="")
    parser.add_argument("--inject_gt_example", default=False)
    # Document selection
    parser.add_argument("--document_pool_type", default="long")
    parser.add_argument("--document_selection_file", default="")
    parser.add_argument("--num_documents", default=0)
    # Use hint & rules
    parser.add_argument("--use_hint", default=True)
    parser.add_argument("--use_rules", default=True)
    # Table retrieval. Use --tbr_selection_file, for retrieval with TBR simulation.
    parser.add_argument(
        "--extra_top_k",
        help="Retrieve extra tables outside the DB to guarantee 'k' tables.",
        default=0)
    # filtered_schema_file dict (csv) from CHESS column selection
    # column names: question_id,selected_schema_with_connections
    # this contains filtered database schema by question_id (key)
    parser.add_argument("--filtered_schema_file", default="")
    parser.add_argument("--db_tbl_col_vals_file", default="db_tbl_col_vals.pickle")
    parser.add_argument("--tbr_selection_file", default="")

    args = parser.parse_args()

    all_in_one_dev_file = os.path.join(DATA_PATH, "example_text2sql_dev.json")
    process = ProcessSqlData(
        input_data_file=args.input_data_path,
        input_table_file=args.input_table_path,
        db_folder_path=args.db_folder_path,
        train_file="",
        dev_file=all_in_one_dev_file,  # output data file
        extra_top_k=int(args.extra_top_k),
        num_examples=int(args.num_examples),
        synthetic_examples=bool(int(args.synthetic_examples)),
        column_description=bool(int(args.column_description)),
        column_examples=bool(int(args.column_examples)),
        use_column_filtering=bool(int(args.use_column_filtering)),
        num_col_values=int(args.num_col_values),
        filtered_schema_file=args.filtered_schema_file,
        db_tbl_col_vals_file=args.db_tbl_col_vals_file,
        vertex_ai_project_id="400355794761",  # change appropriately
        tbr_selection_file=args.tbr_selection_file,
        use_hint=bool(int(args.use_hint)),
        use_rules=bool(int(args.use_rules)),
        example_pool_type=args.example_pool_type,
        example_selection_file=args.example_selection_file,
        inject_gt_example=args.inject_gt_example,
        document_pool_type=args.document_pool_type,
        document_selection_file=args.document_selection_file,
        num_documents=int(args.num_documents),
    )
    process.create_sft_raw_data()
