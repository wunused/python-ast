import ast
import cli
from cli import args, global_dictionary, moduleName, parentPath, paused_queue
from pathlib import Path
import sys
from cli import level
import builtins

def main ():
    args
    masterAnalyzer(parentPath / moduleName)
    while global_dictionary["paused_classes"]:
        for classInstance in global_dictionary["paused_classes"].values():
            paused_resolver(classInstance)
    cli.main()

def masterAnalyzer(modulePath):
    if str(modulePath) in global_dictionary["modules_dictionary"]:
        return
    with open(modulePath, "r") as source:
        tree = ast.parse(source.read())
    subAnalyzerInstance = subAnalyzer(modulePath)
    subAnalyzerInstance.visit(tree)
    level.pop()

def paused_resolver(classInstance):
    if classInstance.finished:
        return
    else:
        for paused in classInstance.paused_objects:
            inner_paused_resolver(paused, classInstance)
        classInstance.finished = True
        del global_dictionary["paused_classes"][classInstance.name]

def inner_paused_resolver(paused, classInstance):
    if global_dictionary["classes_dictionary"][paused.fullName].finished:
        get_inherited_objects(paused.classInstance, paused.fullName)
        classInstance.paused_objects.remove(paused)
    else:
        paused_resolver(global_dictionary["classes_dictionary"][paused.fullName])
        inner_paused_resolver(paused, classInstance)

class subAnalyzer(ast.NodeVisitor):
    def __init__(self, modulePath):
        self.module_level = global_dictionary["modules_dictionary"][str(modulePath)] = moduleInfo(str(modulePath))
        level.push(self.module_level)
        self.parentPath = modulePath.parent

    def visit_Import(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        level.push(classInfoBuilder(node))
        self.generic_visit(node)
        level.pop()

    def visit_FunctionDef(self, node):
        level.push(functionInfoBuilder(node))
        self.generic_visit(node)
        level.pop()

#    def visit_arguments(self, node):
#        get_args(self, node)
#        self.generic_visit(node)

def importInfoBuilder(analyzer, node):
    for alias in node.names:
        upperImportInfo = importInfo(
                alias.name,
                getattr(alias, "asname", None),
                getattr(node, "module", None),
                analyzer.parentPath)
        level.current_level().imports[upperImportInfo.name] = upperImportInfo

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

def classInfoBuilder(node):
    level.current_level().classes[level.current_level().name + "." + node.name] = classInstance = ClassInfo(level.current_level().name + "." + node.name)
    global_dictionary["classes_dictionary"][classInstance.name] = classInstance
    return getInheritance(node, classInstance)

def functionInfoBuilder(node):
    level.current_level().functions[level.current_level().name + "." + node.name] = functionInstance = FunctionInfo(level.current_level().name + "." + node.name, level.current_level())
    global_dictionary["functions_dictionary"][level.current_level().name + "." + functionInstance.name] = functionInstance
    return functionInstance

def getInheritance(node, classInstance):
    for base in node.bases:
        fullName = asname_to_name(getFullName(base))
        # has "fullName" but not the full path name
        if fullName in dir(builtins) or fullName in global_dictionary["from_builtins"] or classInstance in global_dictionary["classes_inheriting_from_built-ins"]:
            print(f"Skipping built-in class: {fullName}")
            if classInstance not in global_dictionary["classes_inheriting_from_built-ins"]:
                global_dictionary["classes_inheriting_from_built-ins"][classInstance.name] = classInstance
            continue
        if fullName == None:
            breakpoint()
        module = fullName.split(".")[0]
        this_level = level.current_level()
        somebuiltin = False
        if "." not in fullName: # this means either the class was imported or was defined in the same module
            while True:
                if fullName in this_level.imports: #works because the keys dont have full path name since it belongs to that specific object
                    if this_level.imports[module].builtin or this_level.imports[module].jython or this_level.imports[module].platform_specific:
                        somebuiltin = True
                        break
                    fullName = this_level.imports[fullName].module.name + "." + fullName
                    break
                elif (this_level.name + "." + fullName) in this_level.classes:
                    fullName = this_level.classes[this_level.name + "." + fullName].name
                    break
                else:
                    this_level = this_level.parent
                    if this_level is None:
                        raise ValueError(f"Class {fullName} not found in imports or classes. Highest level reached: {level.current_level().name}.")
        else: # dot in fullName
            # look in the imports with checking if module in imports
            while True:
                if module in this_level.imports:
                    if this_level.imports[module].builtin or this_level.imports[module].jython or this_level.imports[module].platform_specific:
                        somebuiltin = True
                        break
                    fullName = this_level.imports[module].module.name + "." + fullName.split(".")[1]
                    break
                else:
                    this_level = this_level.parent
                    if this_level is None:
                        if fullName in global_dictionary["classes_inheriting_from_built-ins"]:
                            print(f"Skipping built-in class: {fullName}")
                            return classInstance
                        #breakpoint()
                        raise ValueError(f"Class {fullName} not found in imports.")
        if somebuiltin:
            classInstance.inherited_classes[fullName] = ClassInfo(fullName, builtin=True)
        else:    
            if fullName in global_dictionary["classes_dictionary"] and global_dictionary["classes_dictionary"][fullName].finished: # and not in some list of paused classes
                get_inherited_objects(classInstance, fullName)
            else:
                classInstance.paused_objects.append(pausedObject(classInstance, fullName))
                print(f"Pausing class {classInstance.name} for later resolution of {fullName}.")
                if classInstance.name not in global_dictionary["paused_classes"]:
                    global_dictionary["paused_classes"][classInstance.name] = classInstance
                    classInstance.finished = False
    return classInstance

def get_inherited_objects(classInstance, fullName):
    classInstance.inherited_classes[fullName] = global_dictionary["classes_dictionary"][fullName]
    classInstance.inherited_functions_by_class[f"Inherited from: {fullName}"] = global_dictionary["classes_dictionary"][fullName].functions
        
    for k, v in global_dictionary["classes_dictionary"][fullName].inherited_classes.items():                
        classInstance.inherited_classes[k] = v
        if v.builtin or v.jython or v.platform_specific:
            continue
        else:
            classInstance.inherited_functions_by_class[f"Inherited from: {k}"] = v.functions

def asname_to_name(formerName):
    if level.current_level().imports:
        for key in level.current_level().imports.values():
            if formerName == key.asname:
                return key.name
            else:
                return formerName
    else:
        return formerName

def getFullName(base):
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return getFullName(base.value) + "." + base.attr
    breakpoint()
    
def get_post_slash(something):
    return something.split("/")[-1] if "/" in something else something

#def get_args(analyzer, node):
#    defaultList = node.defaults
#    defaultListLength = len(defaultList)
#    k = j = 0
#    for innerArg in node.args:
#        if j == len(node.args) - defaultListLength and k < defaultListLength:
#            level.current_level().arguments[innerArg.arg] = ArgumentInfo(innerArg.arg, getFullName(getattr(innerArg, "annotation", None)), defaultList[k].value)
#            k += 1
#        elif k < defaultListLength:
#            level.current_level().arguments[innerArg.arg] = ArgumentInfo(innerArg.arg, getFullName(getattr(innerArg, "annotation", None)))
#            j += 1

class pausedObject():
    def __init__(self, classInstance, fullName):
        self.classInstance = classInstance
        self.fullName = fullName
        self.finished = False

class stackItem():
    def __init__(self):
        self.parent = None
        self.finished = True

class importInfo():
    def __init__(self, name, asname, module, parentPath):
        self.name = name
        self.asname: str = asname
        self.builtin = False
        self.jython = False
        self.platform_specific = False
        tryNumber = -1
        if module != None:
            self.type = "Object"
            if module in sys.builtin_module_names:
                self.builtin = True
            elif is_platform_specific_builtin(module):
                self.platform_specific = True
            elif is_jython_related(module):
                self.jython = True
            else:
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
            if name in sys.builtin_module_names:
                self.builtin = True
            elif is_platform_specific_builtin(name):
                self.platform_specific = True
            elif is_jython_related(name):
                self.jython = True
            else:
                if "." in name:
                    name = name.replace(".", "/")
                    leading_slashes = 0
                    for c in name:
                        if c == "/":
                            leading_slashes += 1
                        else:
                            break
                    name = name[leading_slashes:]
                    if leading_slashes > 1:
                        for _ in range(1, leading_slashes):
                            parentPath = parentPath.parent
                self.modulePath = file_checker(name, parentPath, tryNumber)
                masterAnalyzer(self.modulePath)
                self.module: moduleInfo = global_dictionary["modules_dictionary"][str(self.modulePath)]

    def __repr__(self):
        if args.verbose:
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
                    statement = statement.rstrip()
            return statement
        else:
            statement = f"{self.name} {self.type} "
            if self.asname is not None:
                if self.type == "Object":
                    statement += f"as {self.asname} from {get_post_slash(self.module.name)}"
                else:
                    statement += f"as {self.asname}"
            else:
                if self.type == "Object":
                    statement += f"from {get_post_slash(self.module.name)}"
                else:
                    statement = statement.rstrip()
            return statement

class packageInfo():
    def __init__(self):
        self.constructor: dict[moduleInfo] = {}

class moduleInfo(stackItem):
    def __init__(self, name):
        super().__init__()
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
                if args.verbose:
                    self.classes_list.append(class_instance.name)
                else:
                    self.classes_list.append(get_post_slash(class_instance.name))
        if self.functions:
            for function in self.functions.values():
                self.functions_list.append(function.name)
        if args.verbose:
            return (
                f"\nModule Name:\n    {self.name}\n"
                f"Module Imports:\n    {self.imports_list}\n"
                f"Module Classes:\n    {self.classes_list}\n{self.classes}\n"
                f"Module Functions:\n    {self.functions_list}\n"
            )
        else:
            return (
                f"\nModule Name:\n    {get_post_slash(self.name)}\n"
                f"Module Imports:\n    {self.imports_list}\n"
                f"Module Classes:\n    {self.classes_list}\n{self.classes}\n"
                f"Module Functions:\n    {self.functions_list}\n"
            )

class ClassInfo(stackItem):
    def __init__(self, name, builtin=False, jython=False, platform_specific=False):
        super().__init__()  # Call parent constructor
        self.name = name
        self.imports: dict[importInfo] = {}
        self.classes: dict[ClassInfo] = {}
        self.inherited_classes: dict[ClassInfo] = {}
        self.functions: dict[FunctionInfo] = {}
        self.inherited_functions_by_class: dict[FunctionInfo] = {}
        self.paused_objects: list[pausedObject] = []
        self.printableClassList = []
        self.functions_list = []
        self.inherited_functions_list = []
        self.builtin = builtin
        self.jython = jython
        self.platform_specific = platform_specific

    def __repr__(self):
        if self.inherited_classes:
            for inherited_class in self.inherited_classes.values():
                if args.verbose:
                    self.printableClassList.append(inherited_class.name)
                else:
                    self.printableClassList.append(get_post_slash(inherited_class.name))
        if self.functions:
            for function in self.functions.values():
                if args.verbose:
                    self.functions_list.append(function.name)
                else:
                    self.functions_list.append(get_post_slash(function.name))
        if self.inherited_functions_by_class:
            for inherited_function_dict in self.inherited_functions_by_class.values():
                for inherited_function in inherited_function_dict.values():
                    if args.verbose:
                        self.inherited_functions_list.append(inherited_function.name)
                    else:
                        self.inherited_functions_list.append(get_post_slash(inherited_function.name))
        return (
            f"\n    Functions:\n        {self.functions_list}"
            f"\n    Inherited Classes:\n        {self.printableClassList}"                f"\n    Inherited Functions:\n        {self.inherited_functions_list}\n"
        )

class FunctionInfo(stackItem):
    def __init__(self, name, parent):
        super().__init__()
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
        if args.verbose:
            return(
                f"Name:\n    {self.name}\n"
            )
        else:
            return(
                f"Name:\n    {get_post_slash(self.name)}\n"
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