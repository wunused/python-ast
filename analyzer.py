import ast
from pprint import pprint

def main():
    firstFileName = input("Insert file: ") #just for when it first runs, asks the user for which file they want to analyze
    analyze(firstFileName) #calls the analyze function with said file as argument

class Analyzer(ast.NodeVisitor):
    def __init__(self): #constructor
        pass
    #we only want to check for classes, the classes they inherit from, functions, their imports, and do the same in the modules they import   
    def visit_ClassDef(self, node):
        newClassDefInfo = ClassDefInfo()
        newClassDefInfo.name = node.name
        for base in node.bases: #bases refer to classes they inherit from; could be multiple, which is why it is a for loop
            baseName = getName(base)
            newClassDefInfo.ancestors.append(baseName) #gets name of the bases
            newClassDefInfo.modules.append(baseName.split(".")[1])
        for method in node.body:
            newClassDefInfo.methods.append(method)
        print(newClassDefInfo)
    #def report(self):
    #    pprint(self.stats) #prints out the dictionary

class ClassDefInfo():
    def __init__(self):
        self.modules: list[str] = []
        self.name: str
        self.ancestors: list[str] = []
        self.methods: list[str] = []
    def __repr__(self):
        return (
            f"ClassDefInfo(\n"
            f"  name='{self.name}',\n"
            f"  methods={[m.name if hasattr(m, 'name') else m for m in self.methods]},\n"
            f"  ancestors={self.ancestors},\n"
            f"  modules={self.modules}\n"
            f")"
        )


def getName(base): #each base field could belong to a different class
    if isinstance(base, ast.Name): #check if current base field belongs to Name class in ast (refers to a top level class, the module itself, meaning it goes no deeper than that via attributes)—essentially checking if inherits from something without attributes
        return base.id #return name (stored as id) of class
    if isinstance(base, ast.Attribute): #check if current base field belongs to an attribute
        return getName(base.value) + "." + base.attr #if so, get the class it comes from and itself, the attribute. when dealing with inheritance from attributes, the top level class name is stored in the attribute "id" of the "value" field/attribute
        
def analyze(fileName):
        with open(fileName, "r") as source: #opens the file passed in in readable mode; stores it as source variable
            tree = ast.parse(source.read()) #.read() turns the file's content into a string that the ast module can invoke the parse method on
    
        analyzer = Analyzer() #new instance of Analyzer()
        analyzer.visit(tree) #analyzer visits the tree; visit method looks for each node to then invoke visit_(NodeType) on it; if doesn't find visit_(NodeType) declared in the Analyzer class, it calls self.generic_visit(node), which goes into the next layer and repeats the process
        """analyzer.report() #prints out the dictionary
        
        #having finished completely analyzing the tree:
        if analyzer.stats["Modules"]: #check if the Modules key has anything; if so:
            for module in analyzer.stats["Modules"]:
                analyze(module) #run each module inside the key into the analyze function, ensuring each imported module is analyzed"""

main()