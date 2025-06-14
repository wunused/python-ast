import argparse
from pprint import pprint
from pathlib import Path

global_dictionary = {"modules_dictionary": {},
                    "classes_dictionary": {},
                    "functions_dictionary": {}}

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="analyzes inserted python file")
parser.add_argument("-class_name", help="provides details for a class | Usage: module.class")

args = parser.parse_args()
filePath = Path(args.file_name)

def main():
    non_file_name_args = {k: v for k, v in vars(args).items() if k != "file_name" and v not in (None, False)}
    if not non_file_name_args:
        pprint(global_dictionary["modules_dictionary"][filePath.stem])