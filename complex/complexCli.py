import argparse
from pprint import pprint
from pathlib import Path

global_dictionary = {"packages_dictionary": {},
                    "modules_dictionary": {},
                    "classes_dictionary": {},
                    "functions_dictionary": {},
                    "from_builtins": {},
                    "paused_classes": {},
                    "classes_inheriting_from_built-ins": {}
                    }
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

class queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            raise IndexError("Queue is empty")

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

paused_queue = queue()

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="analyzes inserted python file")
parser.add_argument("-c", "--class_name", help="provides details for a class | Usage: module.class")
parser.add_argument("-f", "--function_name", help="provides details for a function")
parser.add_argument("-m", "--module_name", help="provides details for a module | Usage: module")
parser.add_argument("-v", "--verbose", action="store_true", help="provides verbose output")

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