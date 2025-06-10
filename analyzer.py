import ast

global_dictionary = {"modules_dictionary": {}, 
                    "classes_dictionary": {},
                    "functions_dictionary": {}}

def main ():
    moduleName = input("Insert file name: ").split(".")[0]
    masterAnalyzer(moduleName)
    
    
    print(global_dictionary)
    # look-up below

def masterAnalyzer(moduleName):
    if moduleName in global_dictionary["modules_dictionary"]:
        return
    with open(moduleName + ".py", "r") as source: 
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
    
    """Make it so that it can store the FunctionInfo() 
    object into the class it's in"""
    
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
            f"Module Imports = {self.imports}\n"
            f"Module Classes = {self.classes}\n"
        )

def functionInfoBuilder(analyzer, node):
    analyzer.highestLevel.functions[node.name] = functionInstance = FunctionInfo(node.name, analyzer.highestLevel)
    global_dictionary["functions_dictionary"][functionInstance] = functionInstance
    
    # Find a way to separate from innate methods and inherited ones
class FunctionInfo():
    def __init__(self, name, parent):
        self.name = name
        if isinstance(parent, ClassInfo):
            self.parentType = "Class"
        else:
            self.parentType = "Module"
        self.parent = parent # we're going to need this to later check if a function is inherited or not

def classInfoBuilder(analyzer, node):
    
    # MISSING: Create a case for when it inherits from class within same module
    
    analyzer.highestLevel.classes[analyzer.highestLevel.name + "." + node.name] = classInstance = ClassInfo(analyzer.highestLevel.name + "." + node.name)
    global_dictionary["classes_dictionary"][classInstance.name] = classInstance
    
    # there should be 2 possibilities here: 1 - inherited class is from another module
    """# 2 - inherited class is from same module. because classes cant inherit from 
    classes defined after them in the same module, the inherited class has always 
    already been analyzed"""
    
    for base in node.bases: #bases refer to classes they inherit from; could be multiple, which is why it is a for loop
        fullName = asname_to_name(analyzer, getFullName(base))
        if "." not in fullName:
            if fullName in analyzer.highestLevel.imports:
                fullName = analyzer.highestLevel.imports[fullName].module.name + "." + fullName
            else:
                fullName = analyzer.highestLevel.classes[analyzer.highestLevel.name
                                                        + "." 
                                                        + fullName].name
        # find a way to be able to tell whether or not this comes from the same module or different one
        
        classInstance.inherited_classes[fullName] = global_dictionary["classes_dictionary"][fullName]
        classInstance.inherited_functions[f"Inherited from: {fullName}"] = classInstance.inherited_classes[fullName].functions
    return classInstance

    """
    by the rule of classes, if every inherited
    class has already been analyzed, then all 
    their functions have also been analyzed.
        
    Therefore, whenever we analyze any class, we
    can immediately attach inherited functions into
    an inherited_functions attribute
    """

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
    
    """
    if we agree that it starts at the very last possible 
    module without an import, meaning the following non-import 
    parts of the modules will always inherit from an analyzed class, 
    every base found will have already been analyzed.
    
    That means we need to find a way to search for the existing class
    through the base and add them to a key in an inherited_classes 
    dictionary
    
    Only possible exception is when a class inherits from a class 
    defined in the same module
    """

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
        return (
            f"Import Type = {self.type}\n"
            f"Real Name = {self.name}\n"
            f"User-generated Name = {self.asname}\n"
            f"Module Name = {self.module.name}\n"
        )
main()