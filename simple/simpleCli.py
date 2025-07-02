import argparse
from pprint import pprint
from pathlib import Path

classlist = []

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="analyzes inserted python file")
parser.add_argument("-c", "--class_name", help="provides details for a class | Usage: module.class")
#parser.add_argument("-f", "--function_name", help="provides details for a function")
#parser.add_argument("-m", "--module_name", help="provides details for a module | Usage: module")
#parser.add_argument("-v", "--verbose", action="store_true", help="provides verbose output")

args = parser.parse_args()
filePath = Path(args.file_name)
if filePath.parent == ".":
    parentPath = Path.cwd()
elif (Path.cwd() / filePath).exists():
    parentPath = Path.cwd() / filePath.parent
elif filePath.exists():
    parentPath = filePath.parent
moduleName = filePath.name

def main():
    non_file_name_args = {k: v for k, v in vars(args).items() if k != "file_name" and v not in (None, False)}
    if not non_file_name_args or non_file_name_args == {'verbose': True}:
        moduleOutput(str(parentPath / moduleName))
    else:
        if args.class_name:
            classOutput()
        if args.function_name:
            functionOutput()
        if args.module_name:
            moduleOutput(str(Path.cwd() / Path(args.module_name))) # needs to be changed to handle full paths

def moduleOutput(moduleName):
    pprint(global_dictionary["modules_dictionary"][moduleName])

def classOutput():
    pprint(global_dictionary["classes_dictionary"][str(Path.cwd()) + "/" + args.class_name])

def functionOutput():
    pprint(global_dictionary["functions_dictionary"][args.function_name])