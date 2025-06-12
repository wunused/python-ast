import argparse
from pprint import pprint
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=Path, help="analyzes inserted python file")
    parser.add_argument("-class_name", help="provides details for a class | Usage: module.class")
    return parser.parse_args()

def find_file(file_name: Path, modules: dict):
    # non_file_name_args = {k: v for k, v in vars(args).items() if k != "file_name" and v not in (None, False)}
    if not non_file_name_args:
        pprint(analyzer.global_dictionary["modules_dictionary"][args.file_name.rsplit("/", 1)[-1].split(".")[0]])

#args = parser.parse_args()
