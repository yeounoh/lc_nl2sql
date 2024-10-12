import os
from absl import flags
from absl import app
from typing import Sequence
from tqdm import tqdm
import pandas as pd

_INPUT_PATH = flags.DEFINE_string("input_path",
                                  None,
                                  "Input Path",
                                  required=True)

_OUTPUT_PATH = flags.DEFINE_string("output_path",
                                   None,
                                   "Output Path",
                                   required=True)


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  records = []

  i = 0
  for root, _, files in os.walk(_INPUT_PATH.value):
    for file in tqdm(files):
      if file.endswith(".md"):
        with open(os.path.join(root, file), "r") as f:
          doc = f.read()
          records.append({"doc_id": i, "doc": doc})
          i += 1

  df = pd.DataFrame.from_records(records)
  df.to_parquet(_OUTPUT_PATH.value)


if __name__ == "__main__":
  app.run(main)
