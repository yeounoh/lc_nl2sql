import concurrent.futures
import functools
import json
import logging
import os
import time

import numpy as np
import pandas as pd
from tqdm import tqdm
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import argparse
from pathlib import Path

# Usage
# python lc_nl2sql/data_process/retrieve_similar_examples.py \ 
# --project-id cloud-db-nl2sql --train-only-example-pool-path ~/nl2sql/data/train/train.json \ 
# --queries-path ~/nl2sql/data/dev_20240627/dev.json --output-dir lc_nl2sql/data/bird \ 
# --synthetic-example-pool-path lc_nl2sql/data/bird/synthetic_examples.json
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def _parallelize_apply(df, func, column_name, num_workers=16):
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(tqdm(executor.map(func, df[column_name]), total=len(df)))
        return pd.Series(results, index=df.index)


def load_or_compute_embeddings(data_path, cache_dir, embedding_input_columns=None):
    """Loads embeddings from cache or computes them if not found.

    Args:
        data_path: Path to the raw data.
        cache_dir: The full path to the cache dir.
        embedding_input_columns: columns of dataframe to pass to embedding function

    Returns:
        A DataFrame with embeddings, or None if an error occurs.
    """

    def _load_intermediate_results(filepath):
        if os.path.exists(filepath):
            return pd.read_parquet(filepath)
        return None

    data_path = Path(data_path)
    cache_dir = Path(cache_dir)
    cache_filepath = cache_dir / (data_path.stem + ".parquet")
    df = _load_intermediate_results(cache_filepath)

    if df is None:
        try:
            df = pd.read_json(data_path)
            df["sql_prompt"] = df[embedding_input_columns].apply(
                lambda row: "".join(row.values.astype(str)), axis=1
            )
            df["embedding"] = _parallelize_apply(df, embed_text, "sql_prompt")
            os.makedirs(os.path.dirname(cache_filepath), exist_ok=True)
            df.to_parquet(cache_filepath, index=False)
        except Exception as e:
            print(f"Error computing embeddings: {e}")
            return None
    else:
        print(f"Loaded embeddings from {cache_filepath}")

    return df


def _retry_on_quota_exceeded(max_attempts=30, initial_delay=1.0, backoff_factor=2):
    """A decorator for retrying a function call with an exponential backoff delay

    if the error message contains "Quota exceeded".

    Parameters:
    - max_attempts: Maximum number of attempts
    - initial_delay: Initial delay between retries in seconds
    - backoff_factor: Factor by which the delay increases after each retry
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if "Quota exceeded" in str(e) and attempts < max_attempts:
                        logging.warning(
                            f"Quota exceeded, retrying {attempts} time in {delay} seconds."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logging.error(
                            f"Final attempt failed or error not related to quota. {e}"
                        )
                        raise e

        return wrapper

    return decorator


@_retry_on_quota_exceeded(max_attempts=30, initial_delay=1.0, backoff_factor=2)
def embed_text(
    text: str,
    model_name: str = "text-embedding-004",
    task_type: str = "SEMANTIC_SIMILARITY",
) -> list:
    model = TextEmbeddingModel.from_pretrained(model_name)
    text_embedding_input = TextEmbeddingInput(task_type=task_type, text=text)
    embeddings = model.get_embeddings([text_embedding_input])
    return embeddings[0].values


def _brute_force_search_query(query_vector, database_vectors, database_ids, top_k):
    similarities = [cosine_similarity(query_vector, vec) for vec in database_vectors]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [database_ids[i] for i in top_indices]


def _brute_force_similarity_search(
    query_df,
    example_pool_df,
    embedding_col="embedding",
    id_col="example_id",
    top_k=300,
):

    query_vectors = np.array(query_df[embedding_col].tolist())
    database_vectors = np.array(example_pool_df[embedding_col].tolist())
    database_ids = example_pool_df[id_col].tolist()
    num_queries = query_vectors.shape[0]
    results = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        futures = [
            executor.submit(
                _brute_force_search_query,
                query,
                database_vectors,
                database_ids,
                top_k,
            )
            for query in query_vectors
        ]
        for future in tqdm(concurrent.futures.as_completed(futures), total=num_queries):
            results.append(future.result())
    return results


def get_similar_examples(queries_df, example_pool_df, dev_mode=False, top_k=100):
    """Retrieves similar examples for each query."""

    top_example_ids = _brute_force_similarity_search(
        queries_df, example_pool_df, top_k=top_k
    )

    sql_prompt_sql_pairs = []
    for i, query_results in enumerate(top_example_ids):
        query_db = queries_df["db_id"].iloc[i]
        question_id = queries_df["question_id"].iloc[i]
        query_pairs = []

        if dev_mode:
            try:
                query_results.remove(
                    question_id
                )  # remove self if dev mode, assuming id is same as question_id
            except ValueError:
                pass

        for example_id in query_results:
            try:
                pool_row = example_pool_df[example_pool_df["example_id"] == example_id]
                # if pool_row['db_id'].iloc[0] == query_db and question_id!=example_id:  #db check and prevent self retrieval in dev mode
                query_pairs.append(
                    {
                        "sql_prompt": pool_row["sql_prompt"].to_numpy()[0],
                        "sql": pool_row["SQL"].to_numpy()[0],
                    }
                )
            except IndexError:
                print(f"Example ID {example_id} not found.")

        sql_prompt_sql_pairs.append(query_pairs)

    return sql_prompt_sql_pairs


def main(args):

    vertexai.init(project=args.project_id, location=args.location)

    cache_dir = Path(args.output_dir) / "cache"

    train_only_example_pool = load_or_compute_embeddings(
        args.train_only_example_pool_path,
        cache_dir,
        embedding_input_columns=["question", "evidence"],
    )
    synthetic_example_pool = load_or_compute_embeddings(
        args.synthetic_example_pool_path,
        cache_dir,
        embedding_input_columns=["sql_prompt"],
    )
    dev_example_pool = load_or_compute_embeddings(
        args.queries_path, cache_dir, embedding_input_columns=["question", "evidence"]
    )
    queries = dev_example_pool.copy()

    train_and_synthetic_example_pool = pd.concat(
        [train_only_example_pool, synthetic_example_pool]
    )

    # add a unique example_id column to example_pools
    train_only_example_pool["example_id"] = range(len(train_only_example_pool))
    synthetic_example_pool["example_id"] = range(len(synthetic_example_pool))
    dev_example_pool["example_id"] = dev_example_pool["question_id"]
    train_and_synthetic_example_pool["example_id"] = range(
        len(train_and_synthetic_example_pool)
    )

    # assume each example_pool has 'db_id', 'example_id', 'sql_prompt', 'SQL' columns
    train_only_similar_examples = get_similar_examples(
        queries, train_only_example_pool, dev_mode=False, top_k=args.top_k
    )
    synthetic_similar_examples = get_similar_examples(
        queries, synthetic_example_pool, dev_mode=False, top_k=args.top_k
    )
    train_and_synthetic_similar_examples = get_similar_examples(
        queries, train_and_synthetic_example_pool, dev_mode=False, top_k=args.top_k
    )
    dev_only_similar_examples = get_similar_examples(
        queries, dev_example_pool, dev_mode=True, top_k=args.top_k+1
    )

    queries["selected_train_only_examples"] = train_only_similar_examples
    queries["selected_synthetic_only_examples"] = synthetic_similar_examples
    queries["selected_dev_only_examples"] = dev_only_similar_examples
    queries["selected_train_and_synthetic_examples"] = (
        train_and_synthetic_similar_examples
    )

    # save file
    queries.to_json(
        Path(args.output_dir) / "similar_examples.json", index=False, orient="records"
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate similar examples for a set of queries."
    )
    parser.add_argument(
        "--project-id", type=str, required=True, help="Your Google Cloud Project ID"
    )
    parser.add_argument(
        "--location", type=str, default="us-central1", help="Vertex AI location"
    )
    parser.add_argument(
        "--train-only-example-pool-path",
        type=str,
        required=True,
        help="Path to the training example pool file",
    )
    parser.add_argument(
        "--synthetic-example-pool-path",
        type=str,
        required=True,
        help="Path to the synthetic example pool file",
    )
    parser.add_argument(
        "--queries-path", type=str, required=True, help="Path to the queries file"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save the output JSON file",
    )
    parser.add_argument(
        "--top-k", type=int, default=100, help="Number of similar examples to retrieve"
    )

    args = parser.parse_args()

    main(args)
