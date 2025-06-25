import ast
import cli
from cli import args, global_dictionary, filePath
from pathlib import Path
import sys


#start:

def main ():
    args
    if filePath.parent == ".":
        parentPath = Path.cwd()
    elif (Path.cwd() / filePath).exists():
        parentPath = Path.cwd() / filePath.parent
    elif filePath.exists():
        parentPath = filePath.parent
    moduleName = filePath.name
    masterAnalyzer(parentPath / moduleName)
    cli.main()

def masterAnalyzer(modulePath):
    if str(modulePath) in global_dictionary["modules_dictionary"]:
        return
    # this can't open a package
    with open(modulePath, "r") as source:
        tree = ast.parse(source.read())
    subAnalyzerInstance = subAnalyzer(modulePath)
    subAnalyzerInstance.visit(tree)

class subAnalyzer(ast.NodeVisitor):
    def __init__(self, modulePath):
        self.highestLevel = global_dictionary["modules_dictionary"][str(modulePath)] = moduleInfo(str(modulePath))
        self.parentPath = modulePath.parent

    def visit_Import(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classPreviousLevel = self.highestLevel
        self.highestLevel = classInfoBuilder(self, node)
        self.generic_visit(node)
        self.highestLevel = self.classPreviousLevel

    def visit_FunctionDef(self, node):
        self.functionPreviousLevel = self.highestLevel
        self.highestLevel = functionInfoBuilder(self, node)
        self.generic_visit(node)
        self.highestLevel = self.functionPreviousLevel

#    def visit_arguments(self, node):
#        get_args(self, node)
#        self.generic_visit(node)

def importInfoBuilder(analyzer, node):
    for alias in node.names:
        if alias.name in sys.builtin_module_names or getattr(node, "module", None) in sys.builtin_module_names:
            print(f"Skipping builtin module: {alias.name}")
            continue
        upperImportInfo = importInfo(
            alias.name,
            getattr(alias, "asname", None),
            getattr(node, "module", None),
            analyzer.parentPath)
        analyzer.highestLevel.imports[upperImportInfo.name] = upperImportInfo

def file_checker(moduleName, parentPath, tryNumber):
    file_path = parentPath / Path(moduleName + ".py")
    package_constructor_path = parentPath / Path(moduleName + "/__init__.py")
    if file_path.exists():
        return file_path
    elif package_constructor_path.exists():
        #global_dictionary[][str(parentPath / moduleName)] = packageInfo(package_constructor_path)
        return package_constructor_path
    else:
        if tryNumber >= len(sys.path) - 1:
            raise FileNotFoundError(f"Module {moduleName} not found in the specified paths.")
        tryNumber += 1
        return file_checker(moduleName, sys.path[tryNumber], tryNumber)

def classInfoBuilder(analyzer, node):
    analyzer.highestLevel.classes[analyzer.highestLevel.name + "." + node.name] = classInstance = ClassInfo(analyzer.highestLevel.name + "." + node.name)
    global_dictionary["classes_dictionary"][classInstance.name] = classInstance

    for base in node.bases: 
        fullName = asname_to_name(analyzer, getFullName(base))
        if "." not in fullName:
            if fullName in analyzer.highestLevel.imports:
                fullName = analyzer.highestLevel.imports[fullName].module.name + "." + fullName
            else:
                fullName = analyzer.highestLevel.classes[analyzer.highestLevel.name + "." + fullName].name
        classInstance.inherited_classes[fullName] = global_dictionary["classes_dictionary"][fullName]
        classInstance.inherited_functions_by_class[f"Inherited from: {fullName}"] = global_dictionary["classes_dictionary"][fullName].functions
        
        for k, v in global_dictionary["classes_dictionary"][fullName].inherited_classes.items():
            classInstance.inherited_classes[k] = v
            classInstance.inherited_functions_by_class[f"Inherited from: {k}"] = v.functions
    return classInstance

def functionInfoBuilder(analyzer, node):
    analyzer.highestLevel.functions[analyzer.highestLevel.name + "." + node.name] = functionInstance = FunctionInfo(analyzer.highestLevel.name + "." + node.name, analyzer.highestLevel)
    global_dictionary["functions_dictionary"][analyzer.highestLevel.name + "." + functionInstance.name] = functionInstance
    return functionInstance

def asname_to_name(analyzer, formerName):
    for key in analyzer.highestLevel.imports.values():
        if formerName == key.asname:
            return key.name
        else:
            return formerName

def getFullName(base):
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return getFullName(base.value) + "." + base.attr

#def get_args(analyzer, node):
#    defaultList = node.defaults
#    defaultListLength = len(defaultList)
#    k = j = 0
#    for innerArg in node.args:
#        if j == len(node.args) - defaultListLength and k < defaultListLength:
#            analyzer.highestLevel.arguments[innerArg.arg] = ArgumentInfo(innerArg.arg, getFullName(getattr(innerArg, "annotation", None)), defaultList[k].value)
#            k += 1
#        elif k < defaultListLength:
#            analyzer.highestLevel.arguments[innerArg.arg] = ArgumentInfo(innerArg.arg, getFullName(getattr(innerArg, "annotation", None)))
#            j += 1


class importInfo():
    def __init__(self, name, asname, module, parentPath):
        self.name = name
        self.asname: str = asname
        tryNumber = -1
        if module != None:
            self.type = "Object"
            if "." in module:
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
            self.modulePath = file_checker(module, parentPath, tryNumber)
            masterAnalyzer(self.modulePath)
            self.module: moduleInfo = global_dictionary["modules_dictionary"][str(self.modulePath)]
        else:
            self.type = "Module"
            if "." in name:
                name = name.replace(".", "/")
            self.modulePath = file_checker(name, parentPath, tryNumber)
            masterAnalyzer(self.modulePath)
            self.module: moduleInfo = global_dictionary["modules_dictionary"][str(self.modulePath)]

    def __repr__(self):
        statement = f"{self.name} {self.type} "
        if self.asname is not None:
            if self.type == "Object":
                statement += f"as {self.asname} from {self.module.name}"
            else:
                statement += f"as {self.asname}"
        else:
            if self.type == "Object":
                statement += f"from {self.module.name}"
            else:
                statement.rstrip()
        return statement

class packageInfo():
    def __init__(self):
        self.constructor: dict[moduleInfo] = {}

class moduleInfo():
    def __init__(self, name):
        self.package: packageInfo
        self.name: str = name # should change to be full path
        self.imports: dict[importInfo] = {}
        self.classes: dict = {}
        self.functions: dict = {}
        self.imports_list = []
        self.classes_list = []
        self.functions_list = []

    def __repr__(self):
        if self.imports:
            for import_instance in self.imports.values():
                self.imports_list.append(import_instance.__repr__())
        if self.classes:
            for class_instance in self.classes.values():
                self.classes_list.append(class_instance.name)
        if self.functions:
            for function in self.functions.values():
                self.functions_list.append(function.name)
        return (
            f"\nModule Name:\n    {self.name}\n"
            f"Module Imports:\n    {self.imports_list}\n"
            f"Module Classes:\n    {self.classes_list}\n{self.classes}\n"
            f"Module Functions:\n    {self.functions_list}\n"
        )

class ClassInfo():
    def __init__(self, name):
        self.name = name
        self.classes: dict[ClassInfo] = {}
        self.inherited_classes: dict[ClassInfo] = {}
        self.functions: dict[FunctionInfo] = {}
        self.inherited_functions_by_class: dict[FunctionInfo] = {}
        self.printableClassList = []
        self.functions_list = []
        self.inherited_functions_list = []

    def __repr__(self):
        if self.inherited_classes:
            for inherited_class in self.inherited_classes.values():
                self.printableClassList.append(inherited_class.name)
        if self.functions:
            for function in self.functions.values():
                self.functions_list.append(function.name)
        if self.inherited_functions_by_class:
            for inherited_function_dict in self.inherited_functions_by_class.values():
                for inherited_function in inherited_function_dict.values():
                    self.inherited_functions_list.append(inherited_function.name)
        return (
            f"\n    Functions:\n        {self.functions_list}"
            f"\n    Inherited Classes:\n        {self.printableClassList}"
            f"\n    Inherited Functions:\n        {self.inherited_functions_list}\n"
        )

class FunctionInfo():
    def __init__(self, name, parent):
        self.name = name
        self.classes: dict[ClassInfo] = {}
        self.functions: dict[FunctionInfo] = {}
        self.imports: dict[importInfo] = {}
        # self.arguments: dict[ArgumentInfo] = {}
        if isinstance(parent, ClassInfo):
            self.parentType = "Class"
        else:
            self.parentType = "Module"
        self.parent = parent

    def __repr__(self):
        return(
            f"Name:\n    {self.name}\n"
        )

#class ArgumentInfo():
#    def __init__(self, name, annotation, default = None):
#        self.name = name
#        self.annotation = annotation
#        self.default = default
#    def __repr__(self):
#        return(
#            f"\nName = {self.name}\n"
#            f"Annotation = {self.annotation}\n"
#            f"Default Value = {self.default}\n"
#        )

if __name__ == '__main__':
    main()