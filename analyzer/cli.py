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
parser.add_argument("-v", "-venv", help="allows for virtual environment analysis—no activation needed")

args = parser.parse_args()
def relative_resolver(arg):
    filePath = Path(arg)
    if filePath.parent == ".":
        parentPath = Path.cwd()
    elif (Path.cwd() / filePath).exists():
        parentPath = Path.cwd() / filePath.parent
    elif filePath.exists():
        parentPath = filePath.parent
    moduleName = filePath.name
    return parentPath, moduleName
file_name_parentPath, file_name_moduleName = relative_resolver(args.file_name)
if args.v:
    v_parentPath, v_moduleName = relative_resolver(args.v)
    args.v = v_parentPath / v_moduleName