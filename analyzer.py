import ast

instanceList: list[str] = []
analyzedModule = set()
analyzedClass = set()

def main():
    firstFileName = input("Insert file: ") 
    analyze(firstFileName)
    
    for instance in instanceList:
        print(instance)
        for inherited_class in instance.inherited_classes:
            for instance2 in instanceList:
                if inherited_class == instance2.name:
                    instance.methods.extend(instance2.methods)
                    print(instance)

class importAnalyzer(ast.NodeVisitor):
    def __init__(self, fileName):
        self.upperModule = moduleInfo(fileName)
        modules_dictionary[fileName] = self.upperModule

    def visit_Import(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        importInfoBuilder(self, node)
        self.generic_visit(node)

class Analyzer(ast.NodeVisitor):
    def __init__(self, fileName):
        self.upperModule = moduleInfo(fileName)
        modules_dictionary[fileName] = self.upperModule
    def visit_ClassDef(self, node):
        newClassDefInfo = ClassDefInfo(node.name, self.upperModule.imports)
        for base in node.bases: #bases refer to classes they inherit from; could be multiple, which is why it is a for loop
            baseName = getName(base) #gets name of the bases
            newClassDefInfo.base_names.append(baseName)
            if "." not in baseName and baseName != "object":
                newClassDefInfo.moduleFileNames.append(baseName)
            elif baseName != "object":
                newClassDefInfo.moduleFileNames.append(baseName.split(".")[0] + ".py")
                newClassDefInfo.inherited_classes.append(baseName.split(".")[1])
        for method in node.body:
            newClassDefInfo.methods.append(method)

def importInfoBuilder(analyzer, node):
    for alias in node.names:
            upperImportInfo = importInfo(
                alias.name, 
                getattr(alias, "asname", None), 
                getattr(node, "module", None))

            analyzer.upperModule.imports.append(upperImportInfo)

# Dictionary for Lookup:

modules_dictionary = {} # create a new key for every moduleInfo() with key being .name

# CLASSES FOR NODE TYPES:

# Module Node:
class moduleInfo():
    def __init__(self, name):
        self.name: str = name
        self.imports: list[importInfo] = [] # use dictionaries to look up by name
        self.classes: list[ClassDefInfo] = []
        self.methods: list[methodDefInfo] = []

# Import Node:

class importInfo():
    def __init__(self, name, asname, fromInfo):
        if fromInfo != None:
            self.fromInfo = self.module
        self.name: str = name # the name of the imported thing
        self.asname: str = asname # the asname of the imported thing
        self.module: moduleInfo

# Class Node:

class ClassDefInfo():
    def __init__(self, name: str, importInfoList: list[importInfo]):
        for i in importInfoList:
            if i.module.name + "." + i.asname == self.inherited_classes_fullNames or i.asname == self.inherited_classes_fullNames:
                self.inherited_classes_fullNames = i.module.name + "." + i.name
        instanceList.append(self)
        self.name: str = name
        self.inherited_classes_fullNames: list[str] = []
        self.methods: list[str] = []

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

# Method Node:

class methodDefInfo:
    def __init__(self):
        pass
def getName(base):
    
    # some checker for whether or not inherited class was imported (rough sketch)
        
        #if it is inherited

            # if it comes as a full name (module.class)

                # if it comes as alias.class
            
            #if it comes as a class

                #if the class is an alias
    
    if isinstance(base, ast.Name): 
        return base.id 
    if isinstance(base, ast.Attribute): 
        return getName(base.value) + "." + base.attr 
        
def analyze(fileName):
        if fileName in analyzedModule: 
            return
        
        with open(fileName, "r") as source: 
            tree = ast.parse(source.read()) 
        analyzer = Analyzer(fileName)
        analyzer.visit(tree) 
        analyzedModule.add(fileName)
        
        for classInstance in instanceList:
            if classInstance.name not in analyzedClass: 
                for element in classInstance.moduleFileNames:
                    analyze(element + ".py")
                analyzedClass.add(classInstance.name)
main()