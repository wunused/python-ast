import ast

global_dictionary = {"modules_dictionary": {}, "classes_dictionary": {}}

def main ():
    moduleName = input("Insert file name: ").split(".")[0]
    masterAnalyzer(moduleName)
    
    # look-up below
    
    

def masterAnalyzer(moduleName):
    if moduleName in global_dictionary["modules_dictionary"]:
        return
    with open(moduleName + ".py", "r") as source: 
        tree = ast.parse(source.read())
    importAnalyzer = ImportAnalyzer(moduleName)
    importAnalyzer.visit(tree)
    
    """for module in importAnalyzer.upperModule.imports.values():
        masterAnalyzer(module.name)"""

class ImportAnalyzer(ast.NodeVisitor):
    def __init__(self, moduleName):
        global_dictionary["modules_dictionary"][moduleName] = self.upperModule = moduleInfo(moduleName)

    def visit_Import(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        classInfoBuilder(self, node)
        self.generic_visit(node)

class moduleInfo():
    def __init__(self, name):
        self.name: str = name
        self.imports: dict[importInfo] = {} # use dictionaries to look up by name
        self.classes: dict = {}
        self.methods: dict = {}
        
def classInfoBuilder(analyzer, node):
    analyzer.upperModule.classes[node.name] = ClassInfo(analyzer.upperModule.name + "." + node.name)
    for base in node.bases: #bases refer to classes they inherit from; could be multiple, which is why it is a for loop
        baseName = getName(base) #gets name of the bases
    inherited_classes 
    
    
    """if we agree that it starts at the very last possible 
    module without an import, meaning the following non-import 
    parts of the modules will always inherit from an analyzed class, 
    every base found will have already been analyzed.
    
    That means we need to find a way to search for the existing class
    through the base and add them to a key in an inherited_classes 
    dictionary
    """
    
    
    
class ClassInfo():
    def __init__(self, name):
        self.name = name
        self.inherited_classes: dict[ClassInfo] = {}
        
        # some checker for bases comparing to the module.Name 

    def __repr__(self):
        return (
            f"ClassDefInfo(\n"
            f"  name='{self.name}',\n"
            f"  methods={[m.name for m in self.methods]},\n"
            f"  base_names={self.base_names},\n"
            f"  moduleFileNames={self.moduleFileNames}\n"
            f"  inherited_classes={self.inherited_classes}\n"
            f")"
        )

def importInfoBuilder(analyzer, node):
    for alias in node.names:
            upperImportInfo = importInfo(
                alias.name, 
                getattr(alias, "asname", None), 
                getattr(node, "module", None))
            analyzer.upperModule.imports[upperImportInfo.name] = upperImportInfo

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