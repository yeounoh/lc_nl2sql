import unittest
import pandas as pd
import numpy as np
import os
import json
from lc_nl2sql.data_process.retrieve_similar_examples import (
    get_similar_examples,
)
from unittest.mock import patch


class TestYourScript(unittest.TestCase):

    def setUp(self):
        self.example_pool = pd.DataFrame(
            {
                "example_id": range(5),
                "db_id": ["DB 1"] * 5,
                "sql_prompt": [f"Prompt {i}" for i in range(5)],
                "SQL": [f"SQL {i}" for i in range(5)],
                "embedding": [
                    [0.1, 0.2, 0.3, 0.4, 0.5],
                    [0.2, 0.3, 0.4, 0.5, 0.6],
                    [0.3, 0.4, 0.5, 0.6, 0.7],
                    [0.4, 0.5, 0.6, 0.7, 0.8],
                    [0.5, 0.6, 0.7, 0.8, 0.9],
                ],
            }
        )

        self.query = pd.DataFrame(
            {
                "question_id": [0],
                "db_id": ["DB 1"],
                "sql_prompt": ["Query Prompt"],
                "SQL": ["Query SQL"],
                "embedding": [[0.9, 0.8, 0.7, 0.6, 0.5]],
            }
        )

    def test_get_similar_examples_order(self):
        top_k = 3

        similar_examples = get_similar_examples(
            self.query, self.example_pool, top_k=top_k
        )

        self.assertEqual(len(similar_examples), 1)
        self.assertEqual(len(similar_examples[0]), top_k)

        expected_sqls = ["SQL 4", "SQL 3", "SQL 2"]
        retrieved_sqls = [item["sql"] for item in similar_examples[0]]
        self.assertEqual(retrieved_sqls, expected_sqls)

    def test_get_similar_examples_dev_mode(self):

        combined_pool = pd.concat([self.query, self.example_pool], ignore_index=True)
        combined_pool['example_id'] = range(len(combined_pool))
        top_k = 3
        similar_examples = get_similar_examples(
            self.query, combined_pool, top_k=top_k+1, dev_mode=True
        )
        self.assertEqual(len(similar_examples), 1)
        self.assertEqual(len(similar_examples[0]), top_k)

        expected_sqls = ["SQL 4", "SQL 3", "SQL 2"]
        retrieved_sqls = [item["sql"] for item in similar_examples[0]]
        self.assertEqual(retrieved_sqls, expected_sqls)

        similar_examples = get_similar_examples(
            self.query, combined_pool, top_k=top_k, dev_mode=False
        )
        expected_sqls = ["Query SQL", "SQL 4", "SQL 3"]
        retrieved_sqls = [item["sql"] for item in similar_examples[0]]
        self.assertEqual(retrieved_sqls, expected_sqls)

if __name__ == "__main__":
    unittest.main()
