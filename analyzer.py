import ast
from pprint import pprint

instanceList: list[str] = []
analyzedModule = set()
analyzedClass = set()

def main():
    firstFileName = input("Insert file: ") #just for when it first runs, asks the user for which file they want to analyze
    analyze(firstFileName) #calls the analyze function with said file as argument
    
    for instance in instanceList:
        print(instance)
        for inherited_class in instance.inherited_classes:
            for instance2 in instanceList:
                if inherited_class == instance2.name:
                    instance.methods.extend(instance2.methods)
                    print(instance)

class Analyzer(ast.NodeVisitor):
    def __init__(self): #constructor
        pass
    #we only want to check for classes, the classes they inherit from, functions, their imports, and do the same in the modules they import
    def visit_ClassDef(self, node):
        newClassDefInfo = ClassDefInfo()
        newClassDefInfo.name = node.name
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

class ClassDefInfo():
    
    def __init__(self):
        instanceList.append(self)
        self.moduleFileNames: list[str] = []
        self.name: str
        self.base_names: list[str] = []
        self.inherited_classes: list[str] = []
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

def getName(base): #each base field could belong to a different class
    if isinstance(base, ast.Name): #check if current base field belongs to Name class in ast (refers to a top level class, the module itself, meaning it goes no deeper than that via attributes)—essentially checking if inherits from something without attributes
        return base.id #return name (stored as id) of class
    if isinstance(base, ast.Attribute): #check if current base field belongs to an attribute
        return getName(base.value) + "." + base.attr #if so, get the class it comes from and itself, the attribute. when dealing with inheritance from attributes, the top level class name is stored in the attribute "id" of the "value" field/attribute
        
def analyze(fileName):
        if fileName in analyzedModule: #when re-checking the list of modules, we dont want it to reanalyze the first infinitely
            return
        with open(fileName, "r") as source: #opens the file passed in in readable mode; stores it as source variable
            tree = ast.parse(source.read()) #.read() turns the file's content into a string that the ast module can invoke the parse method on
        analyzer = Analyzer() #new instance of Analyzer()
        analyzer.visit(tree) #analyzer visits the tree; visit method looks for each node to then invoke visit_(NodeType) on it; if doesn't find visit_(NodeType) declared in the Analyzer class, it calls self.generic_visit(node), which goes into the next layer and repeats the process
        analyzedModule.add(fileName)
        
        for classInstance in instanceList:
            if classInstance.name not in analyzedClass: #when re-checking the classes to find the modules, though the modules will shave been safely added to the analyzedModule set to not go infinitely, this ensures it doesn't even have to recheck a class whose all modules have been analyzed, saving time
                for element in classInstance.moduleFileNames:
                    analyze(element)
                analyzedClass.add(classInstance.name)
main()