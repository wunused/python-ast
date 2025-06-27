import argparse
from pprint import pprint
from pathlib import Path

global_dictionary = {"packages_dictionary": {},
                    "modules_dictionary": {},
                    "classes_dictionary": {},
                    "functions_dictionary": {}}

class levelStack():
    def __init__(self):
        self.stack = []

    def push(self, level):
        level.parent = self.current_level()
        self.stack.append(level)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            raise IndexError("Stack is empty")

    def size(self):
        return len(self.stack)
    
    def current_level(self):
        if self.stack:
            return self.stack[-1]
        else:
            return None
    # create a function to get the previous level recursively without popping it
    def previous_level(self):
        if len(self.stack) > 1:
            return self.stack[-2]
        else:
            return None

level = levelStack()

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="analyzes inserted python file")
parser.add_argument("-c", "--class_name", help="provides details for a class | Usage: module.class")
parser.add_argument("-f", "--function_name", help="provides details for a function")
parser.add_argument("-m", "--module_name", help="provides details for a module | Usage: module")

args = parser.parse_args()
filePath = Path(args.file_name)

def main():
    non_file_name_args = {k: v for k, v in vars(args).items() if k != "file_name" and v not in (None, False)}
    if not non_file_name_args:
        moduleOutput(str(Path.cwd() / filePath))
    else:
        if args.class_name:
            classOutput()
        if args.function_name:
            functionOutput()
        if args.module_name:
            moduleOutput(args.module_name)

def moduleOutput(moduleName):
    pprint(global_dictionary["modules_dictionary"][moduleName])

def classOutput():
    pprint(global_dictionary["classes_dictionary"][args.class_name])

def functionOutput():
    pprint(global_dictionary["functions_dictionary"][args.function_name])