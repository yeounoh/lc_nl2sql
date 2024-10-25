import hashlib
import os
import numpy as np
import pandas as pd
from itertools import chain
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    TYPE_CHECKING,
    Generator,
    Literal,
)
from datasets import (
    Dataset,
    DatasetDict,
    concatenate_datasets,
    load_dataset,
    interleave_datasets,
)
from transformers.tokenization_utils import PreTrainedTokenizer

from lc_nl2sql.configs.config import EXT2TYPE, IGNORE_INDEX
from lc_nl2sql.configs.data_args import (
    DEFAULT_PROMPT_DICT,
    ALPACA_PROMPT_DICT,
    SQL_PROMPT_DICT,
)

if TYPE_CHECKING:
    from lc_nl2sql.configs.model_args import ModelArguments
    from lc_nl2sql.configs.data_args import DataArguments
    from datasets import IterableDataset

import logging
logger = logging


def extract_default_prompt_dataset(example: Dict[str, Any]) -> Dict[str, str]:
    # Not random, use pre-defined templates
    if example.get("input", "") != "":
        prompt_template = DEFAULT_PROMPT_DICT["prompt_input"]
    else:
        prompt_template = DEFAULT_PROMPT_DICT["prompt_no_input"]

    # Format prompt with example
    formated_prompt = prompt_template.format(**example)

    return {"input": formated_prompt}


def extract_alpaca_prompt_dataset(example: Dict[str, Any]) -> Dict[str, str]:
    if example.get("input", "") != "":
        prompt_format = ALPACA_PROMPT_DICT["prompt_input"]
    else:
        prompt_format = ALPACA_PROMPT_DICT["prompt_no_input"]
    return {"input": prompt_format.format(**example)}


def extract_sql_prompt_dataset(example: Dict[str, Any]) -> Dict[str, str]:
    if example.get("input", "") != "":
        #prompt_format = SQL_PROMPT_DICT["prompt_input"]
        prompt_format = SQL_PROMPT_DICT["prompt_no_prefix"]
    else:
        prompt_format = SQL_PROMPT_DICT["prompt_no_input"]

    # clip if more than 1m tokens
    s = prompt_format.format(**example)
    if len(s) >= 1000000:
        s = s[:999500] + "\n" + example['input']
    return {"input": prompt_format.format(**example)}


def infer_max_len(
    source_len: int, target_len: int, data_args: "DataArguments"
) -> Tuple[int, int]:
    max_target_len = int(
        data_args.cutoff_len * (target_len / (source_len + target_len))
    )
    max_target_len = max(max_target_len, data_args.reserved_label_len)
    max_source_len = data_args.cutoff_len - max_target_len
    return max_source_len, max_target_len


def load_data(
    dataset_path: str, eval_dataset_size: float = 0.1
) -> Union[Dict[str, Dataset], None]:
    """
    Load a dataset based on its name.

    Args:
        dataset_path: A string representing the path to the dataset to be loaded.

    Returns:
        A dictionary containing the loaded dataset if the dataset exists.
        None if the dataset does not exist.

    Raises:
        NotImplementedError: If the dataset name provided is not implemented yet or if
            the dataset is not released.

    Examples:
        >>> load_data('alpaca')
        {'train': Dataset(...), 'validation': Dataset(...), 'test': Dataset(...)}

    """
    if not os.path.exists(dataset_path):
        # Download dataset from HuggingFace Datasets
        print(
            f"Lodding dataset from huggingface, please ref to https://huggingface.co/datasets/{dataset_path}"
        )
        dataset = load_dataset(dataset_path, cache_dir="~/.cache/huggingface/datasets")
        return dataset
    else:
        # Load dataset from local file
        try:
            print(f"Lodding dataset from local path: {dataset_path}")
            dataset = local_dataset(dataset_path, eval_dataset_size)
            return dataset
        except:
            raise ValueError(f"Error loading dataset from {dataset_path}")


## used in get_dataset
def checksum(data_files: List[str], file_sha1: Optional[str] = None) -> None:
    if file_sha1 is None:
        logger.warning(
            "Checksum failed: missing SHA-1 hash value in dataset_info.json."
        )
        return

    if len(data_files) != 1:
        logger.warning("Checksum failed: too many files.")
        return

    with open(data_files[0], "rb") as f:
        sha1 = hashlib.sha1(f.read()).hexdigest()
        if sha1 != file_sha1:
            logger.warning(
                "Checksum failed: mismatched SHA-1 hash value at {}.".format(
                    data_files[0]
                )
            )


def get_dataset(
    model_args: "ModelArguments", data_args: "DataArguments"
) -> Union["Dataset", "IterableDataset"]:
    max_samples = data_args.max_samples
    all_datasets: List[
        Union["Dataset", "IterableDataset"]
    ] = []  # support multiple datasets

    for dataset_attr in data_args.dataset_list:
        logger.info("Loading dataset {}...".format(dataset_attr))

        if dataset_attr.load_from == "hf_hub":
            data_path = dataset_attr.dataset_name
            data_files = None
        elif dataset_attr.load_from == "script":
            data_path = os.path.join(data_args.dataset_dir, dataset_attr.dataset_name)
            data_files = None
        elif dataset_attr.load_from == "file":
            data_path = None
            data_files: List[str] = []

            if os.path.isdir(
                os.path.join(data_args.dataset_dir, dataset_attr.dataset_name)
            ):  # directory
                for file_name in os.listdir(
                    os.path.join(data_args.dataset_dir, dataset_attr.dataset_name)
                ):
                    data_files.append(
                        os.path.join(
                            data_args.dataset_dir, dataset_attr.dataset_name, file_name
                        )
                    )
                    if data_path is None:
                        data_path = EXT2TYPE.get(file_name.split(".")[-1], None)
                    else:
                        assert data_path == EXT2TYPE.get(
                            file_name.split(".")[-1], None
                        ), "file type does not match."
            elif os.path.isfile(
                os.path.join(data_args.dataset_dir, dataset_attr.dataset_name)
            ):  # single file
                data_files.append(
                    os.path.join(data_args.dataset_dir, dataset_attr.dataset_name)
                )
                data_path = EXT2TYPE.get(dataset_attr.dataset_name.split(".")[-1], None)
            else:
                raise ValueError("File not found.")

            assert data_path, "File extension must be txt, csv, json or jsonl."
            checksum(data_files, dataset_attr.dataset_sha1)
        else:
            raise NotImplementedError

        dataset = load_dataset(
            data_path,
            data_files=data_files,
            split=data_args.split,
            cache_dir=model_args.cache_dir,
            streaming=data_args.streaming,
            use_auth_token=True if model_args.use_auth_token else None,
        )

        if max_samples is not None:
            max_samples_temp = min(len(dataset), max_samples)
            dataset = dataset.select(range(max_samples_temp))

        for column_name in ["prompt", "query", "response", "history"]:  # align datasets
            if (
                getattr(dataset_attr, column_name)
                and getattr(dataset_attr, column_name) != column_name
            ):
                dataset = dataset.rename_column(
                    getattr(dataset_attr, column_name), column_name
                )

        if dataset_attr.system_prompt:  # add system prompt
            if data_args.streaming:
                dataset = dataset.map(lambda _: {"system": dataset_attr.system_prompt})
            else:
                dataset = dataset.add_column(
                    "system", [dataset_attr.system_prompt] * len(dataset)
                )

        all_datasets.append(dataset)

    if len(data_args.dataset_list) == 1:
        return all_datasets[0]
    elif data_args.mix_strategy == "concat":
        if data_args.streaming:
            logger.warning(
                "The samples between different datasets will not be mixed in streaming mode."
            )
        return concatenate_datasets(all_datasets)
    elif data_args.mix_strategy.startswith("interleave"):
        if not data_args.streaming:
            logger.warning(
                "We recommend using `mix_strategy=concat` in non-streaming mode."
            )
        stopping_strategy = (
            "first_exhausted"
            if data_args.mix_strategy.endswith("under")
            else "all_exhausted"
        )
        return interleave_datasets(
            all_datasets,
            data_args.interleave_probs,
            stopping_strategy=stopping_strategy,
        )
    else:
        raise ValueError("Unknown mixing strategy.")


def split_train_eval(
    dataset: Dataset,
    do_eval: bool = False,
    eval_dataset_size: float = 0.1,
    max_eval_samples: int = None,
    do_train: bool = True,
    max_train_samples: int = None,
) -> Dict[str, Dataset]:
    """
    Prepare the training and evaluation datasets for a machine learning model.

    Args:
        dataset (DatasetDict): The complete dataset containing train, validation, and test splits.
        do_eval (bool, optional): Whether to use an evaluation dataset or not. Defaults to False.
        eval_dataset_size (float, optional): The size of the validation set if splitting from the training data.
            Ignored if `do_eval` is False. Defaults to 0.2.
        max_eval_samples (int, optional): The maximum number of samples to keep in the evaluation dataset.
            Ignored if `do_eval` is False or `None`. Defaults to None.
        do_train (bool, optional): Whether to use a training dataset or not. Defaults to True.
        max_train_samples (int, optional): The maximum number of samples to keep in the training dataset.
            Ignored if `do_train` is False or `None`. Defaults to None.

    Returns:
        Dict[str, Dataset]: A dictionary containing the prepared training and evaluation datasets
        (if used), where the keys are 'train' and 'eval', respectively.
    """
    if not isinstance(dataset, DatasetDict):
        raise TypeError("The 'dataset' argument must be a DatasetDict object.")

    train_dataset, eval_dataset = None, None
    # Prepare evaluation dataset
    if do_eval:
        if "eval" in dataset:
            eval_dataset = dataset["eval"]
        else:
            # Split train dataset in train and validation according to `eval_dataset_size`
            print(
                f"Splitting the dataset into train and validation according to `eval_dataset_size`:  {eval_dataset_size}"
            )
            dataset = dataset["train"].train_test_split(
                test_size=eval_dataset_size, shuffle=True, seed=42
            )
            eval_dataset = dataset["test"]

        # Reduce evaluation dataset size (if specified)
        print(
            f"You have set the max_eval_samples: {max_eval_samples}, will do sampling ..."
        )
        if max_eval_samples is not None and len(eval_dataset) > max_eval_samples:
            eval_dataset = eval_dataset.select(np.arange(max_eval_samples))

    # Prepare training dataset
    if do_train:
        train_dataset = dataset["train"]

        # Reduce training dataset size (if specified)
        print(
            f"You have set the max_train_samples: {max_train_samples}, will do sampling ..."
        )
        if max_train_samples is not None and len(train_dataset) > max_train_samples:
            train_dataset = train_dataset.select(np.arange(max_train_samples))

    return train_dataset, eval_dataset

def extract_most_similar_idx(query:List, candidates:List[List], top_k: int) -> List:
    query_arr = np.array(query)
    d = len(query)
    findex = faiss.IndexFlatL2(d)
    candidates_arr = np.array(candidates)
    findex.add(candidates_arr)
    D, I = findex.search(np.array([query_arr]), top_k)
    return I[0,:min(top_k, len(candidates))].tolist()
