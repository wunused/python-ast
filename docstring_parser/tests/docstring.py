import ast
import sys

def extract_types(doc):
    tup = []
    dictionary = {}
    args = False
    returns = False
    parts = doc.strip().split(":")
    for part in parts:
        part = part.strip()
        if "Args" in part:
            args = True
        elif "Returns" in part:
            args = False
            returns = True
        elif args:
            param = part.strip().split(" ")
            length = len(param)
            key = param[length-2]
            val = param[length-1][1:len(param[1])-1]
            dictionary[key] = val
        elif returns:
            tup.append(dictionary)
            tup.append(part)
            returns = False
    return tup

class TypeAnnotator(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        doc = ast.get_docstring(node)
        if doc:
            tup = extract_types(doc)
            arg_types = tup[0]
            return_type = tup[1]

            for arg in node.args.args:
                if arg.arg in arg_types:
                    arg.annotation = ast.Name(id=arg_types[arg.arg], ctx=ast.Load())
            if return_type:
                node.returns = ast.Name(id=return_type, ctx=ast.Load())
        self.generic_visit(node)
        return node

def main():
    try:
        filepath = sys.argv[1]
        output_path = "modified_copy.py"
        with open(filepath, 'r') as f:
            code_content = f.read()
        tree = ast.parse(code_content)

#        typeann = TypeAnnotator()
#        patched_tree = typeann.visit(tree)
#        ast.fix_missing_locations(patched_tree)
#        print(ast.dump(patched_tree, indent=4))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node)
                if doc:
                    tup = extract_types(doc)
                    print(tup)
            if isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node)
                if doc:
                    doc = '"' + doc + '"'
                    print(f"class definition `{node.name}`:", doc)

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except IndexError:
        print("Error: Please provide a file path as a command line argument.")

if __name__ == '__main__':
    main()
