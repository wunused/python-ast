import argparse
from pprint import pprint
from pathlib import Path

classlist = []

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="analyzes inserted python file")
parser.add_argument("-c", "--class_name", help="provides details for a class | Usage: module.class")

args = parser.parse_args()
filePath = Path(args.file_name)
if filePath.parent == ".":
    parentPath = Path.cwd()
elif (Path.cwd() / filePath).exists():
    parentPath = Path.cwd() / filePath.parent
elif filePath.exists():
    parentPath = filePath.parent
moduleName = filePath.name
