from markdownify import markdownify as md
import os
from absl import flags
from absl import app
from typing import Sequence
from tqdm import tqdm

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

  for root, _, files in os.walk(_INPUT_PATH.value):
    for file in tqdm(files):
      if file.endswith(".html"):
        with open(os.path.join(root, file), "r") as f:
          html = f.read()
          try:
            markdown = md(html, heading_style="ATX")
          except Exception as e:
            print(f"Error in {file}: {e}")
            continue
          os.makedirs(os.path.join(_OUTPUT_PATH.value, root), exist_ok=True)
          with open(
              os.path.join(_OUTPUT_PATH.value, root,
                           file.replace(".html", ".md")),
              "w",
          ) as f:
            f.write(markdown)


if __name__ == "__main__":
  app.run(main)
