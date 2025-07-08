#!/usr/bin/env python3

import ast
try:
    from cli import args, file_name_parentPath, file_name_moduleName, classlist, level
except:
    raise FileNotFoundError("Insert a valid path")
if args.v:
    from cli import venvPath
from pathlib import Path
import sys
import builtins
from anytree import Node, RenderTree

def main ():
    args
    non_file_name_args = {k: v for k, v in vars(args).items() if k != "file_name" and v not in (None, False) and k != "v"}
    if not non_file_name_args or non_file_name_args == {'verbose': True}:
        fileClassesPrinter(file_name_parentPath / file_name_moduleName)
        print(f"Classes in {file_name_parentPath / file_name_moduleName}:")
        for className in classlist:
            print(className)
    elif args.class_name:
        specificClassPrinter(file_name_parentPath / file_name_moduleName, args.class_name)
        #breakpoint()
        for pre, fill, node in RenderTree(treeBuilder(level.firstElement)):
            print(f"{pre}{node.name}")
    else:
        fileClassesPrinter(file_name_parentPath / file_name_moduleName)
        for className in classlist:
            specificClassPrinter(file_name_parentPath / file_name_moduleName, className)
            #breakpoint()
            for pre, fill, node in RenderTree(treeBuilder(level.firstElement)):
                print(f"{pre}{node.name}")

def fileClassesPrinter(modulePath):
    with open(modulePath, "r") as module:
        moduleTree = ast.parse(module.read())
    visitor = moduleClassesPrinter_visitor()
    visitor.visit(moduleTree)

class moduleClassesPrinter_visitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        classlist.append(node.name)
        self.generic_visit(node)

def specificClassPrinter(modulePath, className):
    with open(modulePath, "r") as module:
        moduleTree = ast.parse(module.read())
    visitor = specificClass_visitor(modulePath, className, moduleTree)
    visitor.visit(moduleTree)
    if not visitor.class_found:
        visitor.importVisitor = import_visitor(visitor.modulePath, visitor.className)
        visitor.importVisitor.visit(visitor.moduleTree)

class import_visitor(ast.NodeVisitor):
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
        if node.module == None:
            node.module = "."
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
    class FunctionFinder(ast.NodeVisitor):
        def __init__(self, classObject):
            self.classObject = classObject

        def visit_FunctionDef(self, node):
            self.classObject.functions.append(FunctionObject(node.name))
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
        self.class_found = False

    def visit_ClassDef(self, node):
        if node.name == self.className:
            self.class_found = True
            level.push(ClassObject(node.name, self.modulePath))
            if level.previous_level():
                level.previous_level().inherited_classes.append(level.current_level())
                #print(f"appended {level.current_level().name} to {level.previous_level().name}")
            for base in node.bases:
                
                if getFullName(base) in dir(builtins):
                    level.current_level().inherited_classes.append(ClassObject(base.id))
                    continue
                import_DFS_tree(self.modulePath, getFullName(base))
            functionFinder = self.FunctionFinder(level.current_level())
            functionFinder.visit(node)
            for classObject in level.current_level().inherited_classes:
                level.current_level().inherited_functions[classObject.name] = classObject.functions
                for k, v in classObject.inherited_functions.items():
                    if k not in level.current_level().inherited_functions:
                        level.current_level().inherited_functions[k] = v
            #print(f"popped {level.pop().name}; current level is now {level.current_level().name}")
        else:
            self.visited_classes += 1
            if self.visited_classes == self.classNumber:
                self.importVisitor = import_visitor(self.modulePath, self.className)
                self.importVisitor.visit(self.moduleTree)
            else:
                self.generic_visit(node)

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

def classFinder(modulePath, className, moduleName):
    with open(modulePath, "r") as module:
        moduleTree = ast.parse(module.read())
    visitor = import_visitor(modulePath, className, moduleName)
    visitor.visit(moduleTree)

def import_DFS_tree(modulePath, formerName):
    if "." in formerName:
        className = formerName.rsplit(".", 1)[-1]
        moduleName = formerName.rsplit(".", 1)[0]
        return classFinder(modulePath, className, moduleName)
    else:
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

def file_checker(moduleName, parentPath, tryNumber):
    """"
    parentPath is the path to where the import statement to moduleName was found
    checks if there exists in the sam directory the module or a package with the name of the module
    
    if not in the parentPath, it recursively goes through sys.path to check if it's there
    """
    file_path = parentPath / Path(moduleName + ".py")
    package_constructor_path = parentPath / Path(moduleName + "/__init__.py")
    #if package_constructor_path == venvPath / "lib/python3.11/site-packages" / Path(moduleName + "/__init__.py"):
    #    breakpoint()
    if file_path.exists():
        return file_path
    elif package_constructor_path.exists():
        return package_constructor_path
    else:
        if tryNumber >= len(sys.path) - 1:
            breakpoint()
            raise FileNotFoundError(f"Module {moduleName} not found in the specified paths.")
        tryNumber += 1
        # make it so it doesnt assume that site-packages is at the end
        if args.v:
            return file_checker(moduleName, sys.path[tryNumber], tryNumber) if Path(sys.path[tryNumber]).name != "site-packages" else file_checker(moduleName, venvPath / "lib/python3.11/site-packages", tryNumber)
        else:
            return file_checker(moduleName, sys.path[tryNumber], tryNumber)

def treeBuilder(classObject, parent=None):
    if args.path_viewer:
        # If path_viewer is enabled, show the full module path for each class
        label = f"{classObject.name} ({classObject.module})"
    else:
        label = f"{classObject.name} ({classObject.module.name if hasattr(classObject.module, 'name') else classObject.module})"
    classNode = Node(label, parent=parent)
    if args.function_viewer:
        if classObject.functions:
            funcNode = Node("Functions", parent=classNode)
            for func in classObject.functions:
                Node(func.name, parent=funcNode)
        if classObject.inherited_classes:
            inherited_classesNode = Node("Inherited Classes", parent=classNode)
            for inherited_class in classObject.inherited_classes:
                treeBuilder(inherited_class, parent=inherited_classesNode)
    else:
        for inherited_class in classObject.inherited_classes:
            #breakpoint()
            treeBuilder(inherited_class, parent=classNode)
    return classNode

class ClassObject():
    def __init__(self, name, module=None):
        self.name = name
        self.module = module
        if module is None:
            self.module = "builtins"
        self.inherited_classes: list[ClassObject] = []
        self.functions: list[FunctionObject] = []
        self.inherited_functions: dict[FunctionObject] = {}
        self.all_functions: list[FunctionObject] = []

    def __repr__(self):
        return f"ClassObject(name={self.name}, inherited_classes={self.inherited_classes})\n{self.functions})\n"

class FunctionObject():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

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