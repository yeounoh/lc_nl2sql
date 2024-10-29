import pickle
import sqlite3
from lc_nl2sql.configs.config import (CHECKER_TEMPLATE, LITERAL_ERROR_TEMPLATE,
                                      MAJORITY_VOTING, VERIFY_ANSWER, SAFETY_SETTING)
import random
import numpy as np
import pandas as pd
import os, re
import json
import time
from typing import Any, Dict, Generator, List, Optional, Tuple

from lc_nl2sql.configs.model_args import (
    ModelArguments,
    FinetuningArguments,
    GeneratingArguments,
)
from lc_nl2sql.configs.data_args import DataArguments
from transformers import HfArgumentParser

import vertexai
from vertexai.generative_models import GenerativeModel


import logging

logging.basicConfig(level=logging.INFO)


class GeminiModel:

    def __init__(self, project_id="400355794761") -> None:
        vertexai.init(project=project_id, location="us-central1")
        self.model = GenerativeModel(model_name="gemini-1.5-pro-002")  # preview-0514
        self.model2 = GenerativeModel(
            model_name="gemini-1.5-flash-002")

    def _infer_args(self, args: Optional[Dict[str, Any]] = None):
        parser = HfArgumentParser((ModelArguments, DataArguments,
                                   FinetuningArguments, GeneratingArguments))
        if args:
            self.data_args = DataArguments
            self.generating_args = GeneratingArguments
            self.use_self_correction = args.get("use_self_correction", True)
            self.use_disambiguation = args.get("use_disambiguation", True)
            self.use_column_filtering_for_correction = args.get("use_column_filtering_for_correction", False)
            self.measure_self_correction_tokens = args.get("measure_self_correction_tokens", False)
            self.db_folder_path = args.get("db_folder_path", "")
            self.temperature = args.get("temperature", 0.5)
            self.db_tbl_col_vals_file = args.get("db_tbl_col_vals_file", "")
        else:
            (
                model_args,
                self.data_args,
                finetuning_args,
                self.generating_args,
            ) = parser.parse_args_into_dataclasses()
            # Initial generation and error correction uses this.
            # Set to 0.5 by default.
            self.temperature = self.generating_args.temperature
            self.use_self_correction = self.generating_args.use_self_correction
            self.use_disambiguation = self.generating_args.use_disambiguation
            self.use_column_filtering_for_correction = self.generating_args.use_column_filtering_for_correction
            self.measure_self_correction_tokens = self.generating_args.measure_self_correction_tokens
            self.db_folder_path = self.data_args.db_folder_path
            self.db_tbl_col_vals_file = self.data_args.db_tbl_col_vals_file

    def set_temperature(self, temperature):
        self.temperature = temperature
        
    def _count_token(self, prompt):
        try:
            if len(prompt) > 1000000 * 4:
                logging.debug("Over 1m token, returning 1000001 as size")
                return 1000001 
            return self.model.count_tokens(prompt).total_tokens
        except Exception as e:
            logging.debug("Token counting failed, returning 1000001 as size")
            return 1000001
        
    def _compress(self, query, multiplier=3):
        # Remove GitHub URLs using re.sub()
        pattern = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        query = re.sub(pattern, "", query)
        n_reduction = 0
        while len(query) > 1000000 * multiplier and n_reduction < 8:
            processed_lines = []
            for line in query.splitlines():
                if len(line) > 20000:
                    processed_lines.append(line[:-10000])
                else:
                    processed_lines.append(line)
            query = "\n".join(processed_lines)
            n_reduction += 1
        return query
    
    def _remove_col_vals(self, query):
        prefix = query.split(
            "###Table column example values###")[0]
        postfix = "**************************".join(
                query.split().split(
                "###Table column example values###")[1].split(
                "**************************")[1:]
            )
        query = prefix + "**************************" + postfix
        return query

    def _generate_sql(self,
                      query,
                      temperature=0.5,
                      use_flash=False,
                      max_retries=5):
        model = self.model2 if use_flash else self.model
        query = self._compress(query)
        try:
            resp = model.generate_content(query, generation_config={"temperature": temperature}, 
                                          safety_settings=SAFETY_SETTING).text.replace(
                                              "```sql","").replace("```", "\n")
            if "<FINAL_ANSWER>" in resp:
                resp = resp.split("<FINAL_ANSWER>")[1].split(
                    "</FINAL_ANSWER>")[0]
        except Exception as e:
            logging.info(f"{str(e)}, retrying in {30 // max(max_retries, 1)} seconds")
            
            
            time.sleep(30 // max(max_retries, 1))
            if "RECITATION" in str(e):
                json_response = str(e).split("Response:")[1]
                try:
                    response_data = json.loads(json_response)
                    citations = response_data['candidates'][0]['citation_metadata']['citations']

                    # Sort citations by start_index in descending order to avoid index issues
                    citations.sort(key=lambda x: x['start_index'], reverse=True)

                    modified_string = query
                    for citation in citations:
                        start_index = citation['start_index']
                        end_index = citation['end_index']
                        modified_string = modified_string[:start_index] + modified_string[end_index:]
                    logging.info("Fixed RECITATION error")
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    logging.debug(f"Error processing JSON response: {e}")
            elif "PROHIBITED_CONTENT" in str(e):
                logging.error("PROHIBITED_CONTENT: {query}")
                return ""
            if max_retries > 0:
                if ("SQL generation failed for: 400" in str(e) 
                    or "400 Unable to submit request" in str(e)):
                    query = self._remove_col_vals(query)
                return self._generate_sql(query,
                                            temperature + 0.1,
                                            use_flash,
                                            max_retries=max_retries - 1)
            else:
                logging.error(f"SQL generation failed for: {str(e)}")
            return ""
        resp = re.sub(r"^ite\s+", "", resp)
        resp = re.sub('\s+', ' ', resp).strip()
        return resp

    def majority_voting(self, query, candidates):
        should_vote = False
        for c in candidates:
            if c != candidates[0]:
                should_vote = True
                break
        if not should_vote:
            return candidates[0]
        candidates = "\n\n".join([c for c in set(candidates)])
        sql = self._generate_sql(MAJORITY_VOTING.format(input=query,
                                                        candidates=candidates),
                                 use_flash=False)
        return sql
    
    def verify_answer(self, sql, question, schema, use_flash=False):
        prompt = VERIFY_ANSWER.format(sql=sql, question=question, schema=schema)
        return self._generate_sql(prompt, use_flash=use_flash)

    def verify_and_correct(self, query, sql, db_folder_path, qid, return_invalid=True, use_flash=False):
        if not self.use_self_correction or query == "":
            return sql, 0

        def fix_error(s, err):
            context_str = query[query.find("###Table creation statements###"
                                           ):query.find("###Question###")]
            # this should capture the hints.
            input_str = query[query.find("###Question###"):query.find(
                "Now generate SQLite SQL query to answer the given")]
            new_prompt = CHECKER_TEMPLATE.format(context_str, input_str, s,
                                                 err)
            new_sql = self._generate_sql(new_prompt,
                                         use_flash=use_flash,
                                         temperature=self.temperature)
            return new_sql, self._count_token(new_prompt) if self.measure_self_correction_tokens else 0

        def fix_literal_error(s, db_id, tried_sql):
            if s == "":
                return fix_error(s, "INFO:root:")
            with open(self.db_tbl_col_vals_file, 'rb') as file:
                try:
                    tbl_col_vals = pickle.load(file)[db_id]
                except:
                    tbl_col_vals = dict()

            def validate_email(email):
                pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                return re.match(pattern, email) is not None
            
            def extract_table_info(input_string):
                table_info = {}
                tables = re.findall(r"CREATE TABLE (\w+)\s*\((.*?)\);", input_string, re.DOTALL)

                for table_name, table_body in tables:
                    columns = re.findall(r"(\w+)\s+\w+.*?-- examples:\s*(.*?)\s*\|", table_body, re.DOTALL)
                    for column_name, example_values in columns:
                        values = re.findall(r"`(.*?)`", example_values)
                        table_info[f"{table_name}.{column_name}"] = values

                return table_info
            
            def format_col_vals(tbl_col_vals):
                s = ""
                for tbl, col_vals in tbl_col_vals.items():
                    for col, vals in col_vals.items():
                        if len(vals) > 0 and validate_email(vals[0]):
                            continue
                        if len(vals) > 50 and np.mean(
                            [len(v) for v in random.sample(vals, 10)]) > 90:
                            continue
                        s += f'* `{tbl}`.`{col}`: [{",".join(vals[:])}]\n'
                return s
            
            if self.use_column_filtering_for_correction:
                df = pd.read_csv(self.data_args.filtered_schema_file)
                id_name, schema_name = 'question_id', 'selected_schema_with_connections'
                col_selected_schemas = dict()
                for k, v in zip(df[id_name], df[schema_name]):
                    col_selected_schemas[int(k)] = v
                filtered_schema = col_selected_schemas.get(qid, "")
                if filtered_schema:
                    table_info = extract_table_info(filtered_schema)
                    col_vals = ""
                    for key, value in table_info.items():
                        col_vals += f"{key}: {value}\n"
            else:
                col_vals = format_col_vals(tbl_col_vals)
            context_str = query[query.find("###Table creation statements###"
                                           ):query.find("###Question###")]
            # this should capture the hints.
            input_str = query[query.find("###Question###"):query.find(
                "Now generate SQLite SQL query to answer the given")]
            new_prompt = LITERAL_ERROR_TEMPLATE.format(context_str, col_vals,
                                                       input_str,
                                                       "\n".join(tried_sql))
            new_sql = self._generate_sql(new_prompt,
                                         use_flash=use_flash,
                                         temperature=0.9)
            return new_sql, self._count_token(new_prompt) if self.measure_self_correction_tokens else 0

        def isValidSQL(sql, db):
            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            err = ""
            rows = []
            is_valid = True
            try:
                rows = cursor.execute(sql).fetchall()
                if len(rows) == 0:
                    is_valid = False
                    err = "empty results"
            except sqlite3.Warning as warning:
                logging.debug(f"SQLite Warning: {warning}")
                err = str(warning)
                is_valid = False
            except sqlite3.Error as e:
                logging.debug(e)
                err = str(e)
                is_valid = False
            finally:
                if conn:
                    conn.close()
            return is_valid, err, len(rows)

        db_name = query.split("The database (\"")[1].split("\") structure")[0]
        db_path = os.path.join(db_folder_path, db_name) + f"/{db_name}.sqlite"

        # this will tick if --measure_self_correction_tokens is set.
        accumulated_token_count = 0

        _sql = sql
        retry_cnt, max_retries = 0, 5
        valid, err, row_cnt = isValidSQL(_sql, db_path)
        tried_sql = [_sql]
        while not valid and retry_cnt < max_retries:
            if err == "empty results" and self.use_disambiguation:
                _sql, extra_tokens = fix_literal_error(_sql, db_name, tried_sql)
            else:
                _sql, extra_tokens = fix_error(_sql, err)
            accumulated_token_count += extra_tokens
            tried_sql.append(_sql)
            valid, err, row_cnt = isValidSQL(_sql, db_path)
            retry_cnt += 1
        if retry_cnt >= max_retries:
            logging.info(f"Correction failed due to {err}: {_sql}")
            if not return_invalid:
                return "", accumulated_token_count
        return _sql, accumulated_token_count

    def chat(self,
             query: str,
             history: Optional[List[Tuple[str, str]]] = None,
             system: Optional[str] = None,
             **input_kwargs) -> Tuple[str, Tuple[int, int]]:
        try:
            use_flash = False
            if 'use_flash' in input_kwargs and input_kwargs['use_flash']:
                use_flalsh = True
            resp = self._generate_sql(query,
                                      use_flash=use_flash,
                                      temperature=self.temperature)
        except:
            print(f'\n*** {query} resulted in API error...\n')
            resp = ""
        return resp, ()

    def stream_chat(self,
                    query: str,
                    history: Optional[List[Tuple[str, str]]] = None,
                    system: Optional[str] = None,
                    **input_kwargs) -> Generator[str, None, None]:
        raise NotImplementedError("stream_chat is not supported.")
