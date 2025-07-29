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

def extract_attributes(doc):
    dictionary = {}
    attr = False
    parts = doc.strip().split(":")
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        if "Attributes" in part:
            attr = True
        elif attr:
            param = part.strip().split(" ")
            length = len(param)
            key = param[length-2]
            val = param[length-1][1:len(param[1])-1]
            dictionary[key] = val
    return dictionary

class TypeAnnotator(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        doc = ast.get_docstring(node)
        if doc:
            tup = extract_types(doc)
            if not tup:
                return node
            arg_types = tup[0]
            return_type = tup[1]

            for arg in node.args.args:
                if arg.arg in arg_types:
                    arg.annotation = ast.Name(id=arg_types[arg.arg], ctx=ast.Load())
            if return_type:
                node.returns = ast.Name(id=return_type, ctx=ast.Load())
        self.generic_visit(node)
        return node
    def visit_ClassDef(self, node):
        doc = ast.get_docstring(node)
        if doc: 
            dictionary = extract_attributes(doc)
            for name, type_str in reversed(dictionary.items()):
                ann_assign = ast.AnnAssign(
                        target=ast.Name(id=name, ctx=ast.Store()),
                        annotation=ast.Name(id=type_str, ctx=ast.Load()),
                        value=None,
                        simple=1
                )
                node.body.insert(1, ann_assign)
        self.generic_visit(node)
        return node

def main():
    try:
        filepath = sys.argv[1]
        output_path = "modified_copy.py"
        with open(filepath, 'r') as f:
            code_content = f.read()
        tree = ast.parse(code_content)

        typeann = TypeAnnotator()
        patched_tree = typeann.visit(tree)
        ast.fix_missing_locations(patched_tree)
        try:
            new_code = ast.unparse(tree)
        except AttributeError:
            import astunparse
            new_code = astunparse.unparse(tree)

        with open(output_path, 'w') as f:
            f.write(new_code) 

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except IndexError:
        print("Error: Please provide a file path as a command line argument.")

if __name__ == '__main__':
    main()
