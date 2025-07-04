import argparse
from pathlib import Path

classlist = []
firstElement = None

class levelStack():
    def __init__(self):
        self.stack = []

    def push(self, level):
        level.parent = self.current_level()
        self.stack.append(level)
        if len(self.stack) == 1:
            self.firstElement = level

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
parser.add_argument("-c", "--class_name", help="provides class inheritance tree for a specific class")
parser.add_argument("-f", "--function_viewer", action="store_true", help="shows functions in a class")
parser.add_argument("-p", "--path_viewer", action="store_true", help="shows full module path for each class")
parser.add_argument("-a", "--all_classes", action="store_true", help="shows details for all classes in a module")

args = parser.parse_args()
filePath = Path(args.file_name)
if filePath.parent == ".":
    parentPath = Path.cwd()
elif (Path.cwd() / filePath).exists():
    parentPath = Path.cwd() / filePath.parent
elif filePath.exists():
    parentPath = filePath.parent
moduleName = filePath.name
