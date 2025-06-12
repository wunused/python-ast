import ast
import cli
import cliLogic

global_dictionary = {"modules_dictionary": {},
                    "classes_dictionary": {},
                    "functions_dictionary": {}}


def main ():
    # TODO: Change the user interface to take the analysis filename as a
    # command line argument, and the class to analyze.
    # Use the argparse library to register the command line arguments.
    #
    # For example:
    # python3 analyzer.py app.py "app.A"
    
    moduleName = args.file_name.rsplit("/", 1)[-1].split(".")[0]
    #moduleName = input("Insert file name: ").split(".")[0]
    masterAnalyzer(moduleName)
    
    cli.logic()

    # TODO: Print out the analyzed class's inheritance information.
    #
    # Example:
    # python3 analyzer.py app.py "app.A"
    # app.A
    # inherited classes: lib.C
    # methods: a_method, lib.C.c_method1, lib.C.c_method2
    # look-up below

def masterAnalyzer(moduleName):
    if moduleName in global_dictionary["modules_dictionary"]:
        return
    with open(topPath + "/" + moduleName + ".py", "r") as source:
        tree = ast.parse(source.read())
    subAnalyzerInstance = subAnalyzer(moduleName)
    subAnalyzerInstance.visit(tree)

class subAnalyzer(ast.NodeVisitor):
    def __init__(self, moduleName):
        self.highestLevel = global_dictionary["modules_dictionary"][moduleName] = moduleInfo(moduleName)

    def visit_Import(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.previousLevel = self.highestLevel
        self.highestLevel = classInfoBuilder(self, node)
        self.generic_visit(node)
        self.highestLevel = self.previousLevel

    def visit_FunctionDef(self, node):
        functionInfoBuilder(self, node)
        self.generic_visit(node)

class moduleInfo():
    def __init__(self, name):
        self.name: str = name
        self.imports: dict[importInfo] = {} # use dictionaries to look up by name
        self.classes: dict = {}
        self.functions: dict = {}

    def __repr__(self):
        return (
            f"Module Name = {self.name}\n"
            f"Module Imports =\n{self.imports}\n"
            f"Module Classes =\n{self.classes}\n"
        )

def functionInfoBuilder(analyzer, node):
    analyzer.highestLevel.functions[node.name] = functionInstance = FunctionInfo(node.name, analyzer.highestLevel)
    global_dictionary["functions_dictionary"][functionInstance] = functionInstance

class FunctionInfo():
    def __init__(self, name, parent):
        self.name = name
        if isinstance(parent, ClassInfo):
            self.parentType = "Class"
        else:
            self.parentType = "Module"
        self.parent = parent

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
        classInstance.inherited_functions[f"Inherited from: {fullName}"] = classInstance.inherited_classes[fullName].functions
    return classInstance

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

class ClassInfo():
    def __init__(self, name):
        self.name = name
        self.inherited_classes: dict[ClassInfo] = {}
        self.functions: dict[FunctionInfo] = {}
        self.inherited_functions: dict[FunctionInfo] = {}

    def __repr__(self):
        return (
            f"Class Name = {self.name}\n"
            f"Inherited Classes = {self.inherited_classes}\n"
        )

def importInfoBuilder(analyzer, node):
    for alias in node.names:
        upperImportInfo = importInfo(
            alias.name,
            getattr(alias, "asname", None),
            getattr(node, "module", None))
        analyzer.highestLevel.imports[upperImportInfo.name] = upperImportInfo

class importInfo():
    def __init__(self, name, asname, module):
        self.name = name
        self.asname: str = asname
        if module != None:
            self.type = "Object"
            masterAnalyzer(module)
            self.module: moduleInfo = global_dictionary["modules_dictionary"][module]
        else:
            self.type = "Module"
            masterAnalyzer(name)
            self.module: moduleInfo = global_dictionary["modules_dictionary"][name]

    def __repr__(self):
        if self.asname is not None:
            if self.type == "object":
                return (
                    f"\nReal Name = {self.name}\n"
                    f"User-generated Name = {self.asname}\n"
                    f"Import Type = {self.type}\n"
                    f"Module = {self.module.name}"
                )
            else:
                return(
                    f"\nReal Name = {self.name}\n"
                    f"User-generated Name = {self.asname}\n"
                    f"Import Type = {self.type}\n"
                )
        else:
            if self.type == "object":
                return (
                    f"\nName = {self.name}\n"
                    f"Import Type = {self.type}\n"
                    f"Module = {self.module.name}"
                )
            else:
                return(
                    f"\nName = {self.name}\n"
                    f"Import Type = {self.type}\n"
                )

args = cli.parser.parse_args()
topPath = args.file_name.rsplit("/", 1)[0]
main()