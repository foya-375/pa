#!/usr/bin/env python3

import pydantic as pd
from pydantic.types import Path
import typing   as tp
import yaml
import os
import sys

__all__ = ["Configure", "load_config"]

"""
Progress definition, a progress is a combinition of a working directory and a set of commands.
You can edit them in the configuration file like this:

  process_name:
    path: path_to_the_workspace
    commands:
      - cmd1
      - cmd2
The configuration file is located as "~/.pa_conf.yaml"
"""
class Progress(pd.BaseModel):
  name: str
  path: Path # pd.DirectoryPath
  commands: tp.List[str]

# Parse the configuration file, read-in all the progresses
class Configure:
  progress_list = []

  @classmethod
  def load(cls, conf):
    for name, progress in conf.items():
      cls.progress_list.append(Progress(name=name, **progress))

# A simple unique loader that prevents yaml to load duplicated progresses
class UniqueProgressNameChecker(yaml.SafeLoader):
  """
  Raise a exception when there are progresses with duplicated name
  """
  def construct_mapping(self, node, deep=False):
    mapping = set()
    for key_node, value_node in node.value:
      if ':merge' in key_node.tag:
        continue 
      key = self.construct_object(key_node, deep=deep)
      if key in mapping:
        raise ValueError(f"Duplicate {key!r} key found in configuration.")
      mapping.add(key)
    return super().construct_mapping(node, deep)

def load_config():
  conf_path = os.path.join(os.path.expanduser("~"), ".pa_conf.yaml")
  try:
    with open(conf_path, "r", encoding="utf-8") as configuration:
      config = yaml.load(configuration, Loader=UniqueProgressNameChecker)
    Configure.load(config)
  except Exception as error:
    print(f"Error parsing configuration:{error}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
  try:
    load_config()
    prog = next(prog for prog in Configure.progress_list if prog.name == sys.argv[1])

    # Simply pass all the command to stdout, they would be catched by bash script
    print(prog.path)
    for cmd in prog.commands:
      print(cmd)

  except StopIteration:
    print(f"No progress named: {sys.argv[1]}, please correct it.")
    sys.exit(1)
  except Exception as e:
    print(f"Error Executing:{e}", file=sys.stderr)
    sys.exit(1)
