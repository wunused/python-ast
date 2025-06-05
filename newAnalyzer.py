import ast

modules_dictionary = {}

def main ():
    moduleName = input("Insert file name: ").split(".")[0]
    masterAnalyzer(moduleName)

def masterAnalyzer(moduleName):
    if moduleName in modules_dictionary:
        return
    with open(moduleName + ".py", "r") as source: 
        tree = ast.parse(source.read())
    importAnalyzer = ImportAnalyzer(moduleName)
    importAnalyzer.visit(tree)
    
    """for module in importAnalyzer.upperModule.imports.values():
        masterAnalyzer(module.name)"""
    
class ImportAnalyzer(ast.NodeVisitor):
    def __init__(self, moduleName):
        modules_dictionary[moduleName] = self.upperModule = moduleInfo(moduleName)

    def visit_Import(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

class moduleInfo():
    def __init__(self, name):
        self.name: str = name
        self.imports: dict[importInfo] = {} # use dictionaries to look up by name
        self.classes: dict = {}
        self.methods: dict = {}

def importInfoBuilder(analyzer, node):
    for alias in node.names:
            upperImportInfo = importInfo(
                alias.name, 
                getattr(alias, "asname", None), 
                getattr(node, "module", None))
            analyzer.upperModule.imports[upperImportInfo.name] = upperImportInfo
            

class importInfo():
    def __init__(self, name, asname, module):
        if module != None:
            self.name = module
        else:
            self.name = name # the name of the imported thing
        self.asname: str = asname # the asname of the imported thing
        self.module: moduleInfo