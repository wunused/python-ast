import argparse
from pprint import pprint
from pathlib import Path

global_dictionary = {"modules_dictionary": {},
                    "classes_dictionary": {},
                    "functions_dictionary": {}}

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="analyzes inserted python file")
parser.add_argument("-c", "--class_name", help="provides details for a class | Usage: module.class")
parser.add_argument("-f", "--function_name", help="provides details for a function")

args = parser.parse_args()
filePath = Path(args.file_name)

def main():
    non_file_name_args = {k: v for k, v in vars(args).items() if k != "file_name" and v not in (None, False)}
    if not non_file_name_args:
        moduleOutput()
    else:
        if args.class_name:
            classOutput()
        if args.function_name:
            functionOutput()

def moduleOutput():
    pprint(global_dictionary["modules_dictionary"][filePath.stem])

def classOutput():
    pprint(global_dictionary["classes_dictionary"][args.class_name])

def functionOutput():
    pass