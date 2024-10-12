from markdownify import markdownify as md
import os
from absl import flags
from absl import app
from typing import Sequence
from tqdm import tqdm
from typing import Sequence
import re

_INPUT_PATH = flags.DEFINE_string("input_path",
                                  None,
                                  "Input Path",
                                  required=True)

_OUTPUT_PATH = flags.DEFINE_string("output_path",
                                   None,
                                   "Output Path",
                                   required=True)


class ContentBlcok:

  def __init__(self, title, level, ancestors) -> None:
    self.title = title
    self.content = title
    self.level = level
    self.ancestors = ancestors

  def parse(self, lines, content_blocks):
    i = 1
    for i in range(1, len(lines)):
      line = lines[i]
      if line.startswith("#"):

        title = line

        hashtags = re.findall(r'^#+', line)[0]
        num_hashtags = len(hashtags)
        new_context_block = ContentBlcok(
            title=title,
            level=num_hashtags,
            ancestors=self.ancestors[:num_hashtags])
        content_blocks.append(new_context_block)
        new_context_block.parse(lines[i:], content_blocks)
        break
      else:
        self.content += line


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  for root, _, files in os.walk(_INPUT_PATH.value):
    for file in tqdm(files):
      print(file)
      if file.endswith(".md"):
        with open(os.path.join(root, file), "r") as f:
          lines = f.readlines()
          content_blocks = []
          for line in lines:
            if line != '':
              title = line
              break
          content_block = ContentBlcok(title, 0, [])
          content_blocks.append(content_block)
          content_block.parse(lines, content_blocks)

        output_folder = os.path.join(_OUTPUT_PATH.value, root,
                                     file.replace('.md', ''))
        os.makedirs(output_folder, exist_ok=True)
        i = 0
        for content_block in content_blocks:
          with open(
              os.path.join(output_folder, f"{i}.md"),
              "w",
          ) as f:
            f.write(content_block.content)
          i += 1


if __name__ == "__main__":
  app.run(main)
