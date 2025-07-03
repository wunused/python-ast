import ast
from simpleCli import args, moduleName, parentPath, classlist
from pathlib import Path
import sys
import builtins

def main ():
    args
    non_file_name_args = {k: v for k, v in vars(args).items() if k != "file_name" and v not in (None, False)}
    if not non_file_name_args or non_file_name_args == {'verbose': True}:
        fileClassesPrinter(parentPath / moduleName)
    else:
        specificClassPrinter(parentPath / moduleName, args.class_name)

def fileClassesPrinter(modulePath):
    with open(modulePath, "r") as module:
        moduleTree = ast.parse(module.read())
    visitor = moduleClassesPrinter_visitor()
    visitor.visit(moduleTree)
    print(f"Classes in {modulePath}:\n{classlist}")

class moduleClassesPrinter_visitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        classlist.append(node.name)
        self.generic_visit(node)

def specificClassPrinter(modulePath, className):
    with open(modulePath, "r") as module:
        moduleTree = ast.parse(module.read())
    visitor = specificClass_visitor(modulePath, className, moduleTree)
    visitor.visit(moduleTree)

class import_visitor(ast.NodeVisitor):
    # this is where we will go to a new module
    def __init__(self, modulePath, className, moduleName=None):
        self.modulePath = modulePath
        self.className = className
        self.moduleName = moduleName

    def visit_Import(self, node):
        if self.moduleName is None:
            return
        for alias in node.names:
            if "." in alias.name:
                module, parentPath = resolve_path(alias.name, self.modulePath.parent)
            else:
                module = alias.name
                parentPath = self.modulePath.parent
            import_alias_loop(module, parentPath, alias, self.className, self.moduleName)

    def visit_ImportFrom(self, node):
        if "." in node.module:
            module, parentPath = resolve_path(node.module, self.modulePath.parent)
        else:
            module = node.module
            parentPath = self.modulePath.parent
        for alias in node.names:
            importFrom_alias_loop(module, parentPath, alias, self.className)

class specificClass_visitor(ast.NodeVisitor):
    class ClassCounter(ast.NodeVisitor):
        def __init__(self):
            self.classNumber = 0

        def visit_ClassDef(self, node):
            self.classNumber += 1
            self.generic_visit(node)

    def __init__(self, modulePath, className, moduleTree):
        self.classCounter = self.ClassCounter()
        self.moduleTree = moduleTree
        self.classCounter.visit(self.moduleTree)
        self.classNumber = self.classCounter.classNumber
        self.visited_classes = 0
        self.parentPath = modulePath.parent
        self.modulePath = modulePath
        self.className = className
        self.found = False

    def visit_ClassDef(self, node):
        #if self.className == "Tag" and node.name == "Tag":
        #    breakpoint()
        if node.name == self.className:
            self.found = True
            print(f"Found class: {node.name}")
            for base in node.bases:
                import_DFS_tree(self.modulePath, getFullName(base))
        else:
            self.visited_classes += 1
            if self.visited_classes == self.classNumber:
                self.importVisitor = import_visitor(self.modulePath, self.className)
                self.importVisitor.visit(self.moduleTree)
            else:
                self.generic_visit(node)
        # by here should have already finished the dependency tree for fullName
        # first append to some list of inherited classes for this specific class

def import_alias_loop(module, parentPath, alias, className, moduleName):
    if getattr(alias, 'asname', None) == moduleName:
        specificClassPrinter(file_checker(module, parentPath, -1), className)
    elif alias.name == moduleName:
        specificClassPrinter(file_checker(module, parentPath, -1), className)

def importFrom_alias_loop(module, parentPath, alias, className):
    if getattr(alias, 'asname', None) == className:
        specificClassPrinter(file_checker(module, parentPath, -1), alias.name)
    elif alias.name == className:
        specificClassPrinter(file_checker(module, parentPath, -1), alias.name)

def classFinder(modulePath, className):
    with open(modulePath, "r") as module:
        moduleTree = ast.parse(module.read())
    visitor = import_visitor(modulePath, className)
    visitor.visit(moduleTree)

def import_DFS_tree(modulePath, formerName):
    if "." in formerName: # has no asname; class is defined in a different module
        # the actual module could have an asname
        className = formerName.rsplit(".", 1)[-1]
        # we want to find the import statement and go into the module
        # you already have the module name or asname
        return classFinder(modulePath, className)
        # at this point we just wanna jump into a new module!!
        # how do we check if module is name or asname?
    else: # could have an asname; class could be defined in the same module or different one
        return specificClassPrinter(modulePath, formerName)

def resolve_path(module, parentPath):
    module = module.replace(".", "/")
    leading_slashes = 0
    for c in module:
        if c == "/":
            leading_slashes += 1
        else:
            break
    module = module[leading_slashes:]
    if leading_slashes > 1:
        for _ in range(1, leading_slashes):
            parentPath = parentPath.parent
    return module, parentPath

def getFullName(base):
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return getFullName(base.value) + "." + base.attr
    if isinstance(base, ast.Call):
        breakpoint()

# returns a full path
def file_checker(moduleName, parentPath, tryNumber):
    file_path = parentPath / Path(moduleName + ".py")
    package_constructor_path = parentPath / Path(moduleName + "/__init__.py")
    if file_path.exists():
        return file_path
    elif package_constructor_path.exists():
        return package_constructor_path
    else:
        if tryNumber >= len(sys.path) - 1:
            breakpoint()
            raise FileNotFoundError(f"Module {moduleName} not found in the specified paths.")
        tryNumber += 1
        return file_checker(moduleName, sys.path[tryNumber], tryNumber)

PLATFORM_SPECIFIC_BUILTINS = {
    # Windows
    '_winapi', 'msvcrt', 'winsound', '_msi',
    # Unix/Linux/Mac  
    '_posix', '_scproxy', 'grp', 'pwd', 'spwd',
    # Add more as needed
}

def is_platform_specific_builtin(module_name):
    return module_name in PLATFORM_SPECIFIC_BUILTINS

JYTHON_PACKAGES = {
    'org.python.core',
    'org.python.util',
    'org.python.modules',
    'org.python.compiler',
    'org.python.antlr',
    'java.lang',
    'java.util',
    'java.io',
    'javax.',
    'com.sun.',
    'com.oracle.'
}

def is_jython_related(module_name):
    return module_name in JYTHON_PACKAGES

if __name__ == '__main__':
    main()