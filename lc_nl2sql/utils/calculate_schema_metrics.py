import argparse
import sqlite3
import re
import numpy as np
import pandas as pd

# python lc_nl2sql/utils/calculate_schema_metrics.py 
# --selected_schema_file lc_nl2sql/data/bird/col_selection_schema.csv 
# --correct_schema_file lc_nl2sql/data/bird/gt_schema.csv

def _extract_schema_with_sqlite(schema_str):
    """Extracts table and column information from a SQLite schema string"""
    tables = {}

    # Remove comments
    schema_str = re.sub(r"--.*$", "", schema_str, flags=re.MULTILINE)

    # Remove trailing commas within CREATE TABLE statements
    schema_str = re.sub(r",\s*\)", ")", schema_str, flags=re.MULTILINE, count=0)

    # Quote table names in CREATE TABLE statements
    schema_str = re.sub(r"CREATE TABLE (\S+)", r"CREATE TABLE '\1'", schema_str)


    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.executescript(schema_str)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [row[0] for row in cursor.fetchall()]

    for table_name in table_names:
        cursor.execute(f"PRAGMA table_info(`{table_name}`);")
        columns = [row[1] for row in cursor.fetchall()]
        tables[table_name.lower()] = columns

    conn.close()
    return tables

def calculate_metrics(data):
  table_precision = 0
  table_recall = 0
  col_precision = 0
  col_recall = 0
  try:
    correct_schema = data["correct_columns"]
    selected_schema = data["selected_schema"]

    correct_tables = set([key.lower() for key in correct_schema])
    selected_tables = set([key.lower() for key in selected_schema])

    selected_columns = []
    for table_name, cols in selected_schema.items():
      for col in cols:
        selected_columns.append(f"'{table_name.lower()}'.'{col.lower()}'")

    correct_columns = []
    for table_name, cols in correct_schema.items():
      for col in cols:
        correct_columns.append(f"'{table_name.lower()}'.'{col.lower()}'")

    correct_columns = set(correct_columns)
    selected_columns = set(selected_columns)

    if len(selected_tables):
      table_precision = len(correct_tables.intersection(selected_tables)) / len(
          selected_tables
      )

    if len(correct_tables):
      table_recall = len(correct_tables.intersection(selected_tables)) / len(
          correct_tables
      )

    if len(selected_columns):
      col_precision = len(correct_columns.intersection(selected_columns)) / len(
          selected_columns
      )
    if len(correct_columns):
      col_recall = len(correct_columns.intersection(selected_columns)) / len(
          correct_columns
      )
  except Exception as e:
    print(e)

  return table_precision, table_recall, col_precision, col_recall


def calculate_metrics_from_files(selected_schema_file, correct_schema_file):
    """Calculates precision and recall from CSV files."""

    selected_df = pd.read_csv(selected_schema_file)
    correct_df = pd.read_csv(correct_schema_file)

    results = []
    for question_id in correct_df["question_id"].unique():
        try:
            correct_row = correct_df[correct_df["question_id"] == question_id]
            selected_row = selected_df[selected_df["question_id"] == question_id]
            
            selected_schema_str = selected_row["selected_schema_with_connections"].iloc[0]
            correct_schema_str = correct_row["correct_schema_str"].iloc[0]

            if pd.isna(correct_schema_str) or correct_schema_str is np.nan:
              continue
            
            if pd.isna(selected_schema_str) or selected_schema_str is np.nan:
              selected_schema_str = ""
            
            
            
            correct_schema = _extract_schema_with_sqlite(correct_row["correct_schema_str"].iloc[0])
            selected_schema = _extract_schema_with_sqlite(selected_row["selected_schema_with_connections"].iloc[0])

            results.append({
                "question_id": question_id,
                "correct_columns": correct_schema,
                "selected_schema": selected_schema
            })

        except Exception as e:
            print(f"Error processing question ID {question_id}: {e}")

    table_precisions, table_recalls, col_precisions, col_recalls = [], [], [], []
    for data in results:
        tp, tr, cp, cr = calculate_metrics(data)
        table_precisions.append(tp)
        table_recalls.append(tr)
        col_precisions.append(cp)
        col_recalls.append(cr)

    avg_table_precision = sum(table_precisions) / len(table_precisions) if table_precisions else 0
    avg_table_recall = sum(table_recalls) / len(table_recalls) if table_recalls else 0
    avg_col_precision = sum(col_precisions) / len(col_precisions) if col_precisions else 0
    avg_col_recall = sum(col_recalls) / len(col_recalls) if col_recalls else 0


    print(f"Avg Table Precision: {avg_table_precision:.4f}")
    print(f"Avg Table Recall: {avg_table_recall:.4f}")
    print(f"Avg Column Precision: {avg_col_precision:.4f}")
    print(f"Avg Column Recall: {avg_col_recall:.4f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate schema selection metrics.")
    parser.add_argument("--selected_schema_file", help="Path to the CSV file with selected schemas.")
    parser.add_argument("--correct_schema_file", help="Path to the CSV file with correct schemas.")
    args = parser.parse_args()

    calculate_metrics_from_files(args.selected_schema_file, args.correct_schema_file)