import ast
import sys

def google(doc):
    """
    Parses through the docstring and finds type information based on keywords in Google Style Docstrings

    Args:
        doc (str): the function's docstring

    Returns:
        array: an array where the first value is a dictionary of the function's arguments and the second value is the return type specified in the docstring
    """
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
            valwithparens = param[length-1]
            lengthval = len(valwithparens)
            val = valwithparens[1:lengthval-1]
            dictionary[key] = val
        elif returns:
            tup.append(dictionary)
            tup.append(part)
            returns = False
    return tup

def sphinx(doc):
    """
    Parses through the docstring and finds type information based on keywords in Sphinx Style Docstrings

    Args:
       doc (str): the function's docstring

    Returns:
        array: an array where the first value is a dictionary of the function's arguments and the second value is the return type specified in the docstring
    """
    tup = []
    dictionary = {}
    parts = doc.strip().splitlines()
    for part in parts:
        part = part.strip()
        if ":type" in part:
            param = part.split(" ")
            key = param[1][:len(param[1]) - 1]
            dictionary[key] = param[2]
        elif ":rtype:" in part:
            param = part.split(" ")
            tup.append(dictionary)
            tup.append(param[1])
    return tup

def numpy(doc):
    """
    Parses through the docstring and finds type information based on keywords in NumPy Style Docstrings

    Args:
       doc (str): the function's docstring

    Returns:
        array: an array where the first value is a dictionary of the function's arguments and the second value is the return type specified in the docstring
    """
    tup = []
    dictionary = {}
    returns = False
    parts = doc.strip().splitlines()
    for part in parts:
        part = part.strip()
        if ":" in part:
            param = part.split(" ")
            dictionary[param[0]] = param[2]
        elif "Returns" in part:
            returns = True
        elif returns:
            if "-" in part:
                continue
            tup.append(dictionary)
            tup.append(part)
            returns = False
    return tup

def epytext(doc):
    """
    Parses through the docstring and finds type information based on keywords in Epytext Style Docstrings

    Args:
       doc (str): the function's docstring

    Returns:
        array: an array where the first value is a dictionary of the function's arguments and the second value is the return type specified in the docstring
    """
    tup = []
    dictionary = {}
    parts = doc.strip().splitlines()
    for part in parts:
        part = part.strip()
        if "@type" in part:
            param = part.split(" ")
            key = param[1][:len(param[1]) - 1]
            dictionary[key] = param[2]
        elif "@rtype" in part:
            param = part.split(" ")
            tup.append(dictionary)
            tup.append(param[1])
    return tup

def extract_attributes(doc):
    """
    Parses through the docstring and finds type information based on keywords in the class docstring

    Args:
       doc (str): the class's docstring

    Returns:
       dictionary: a dictionary of the attributes of the class
    """
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
    """
    AST transformer that adds type annotations in Python code.

    This class walks through the abstract syntax tree (AST) of Python code and applies type annotations according to the docstring.

    Inherits from:
        ast.NodeTransformer: A base class that enables modifying the AST in place.

    Methods:
        visit_FunctionDef(node):
            Visits a function definition node and adds type annotations on arguments and return types.
        
        visit_ClassDef(node):
            Visits a class definition node and adds type annotations on attributes.
    """
    def visit_FunctionDef(self, node):
        """
        Visits a function definition node and adds type annotations.

        This method analyzes the arguments and return type of a function based on the information from the docstring, and modifies the AST node to include the appropriate type annotations.

        Args:
            node (ast.FunctionDef): The function definition node to process.

        Returns:
            ast.FunctionDef: The potentially modified function definition node with updated type annotations.
        """
        doc = ast.get_docstring(node)
        doc_type = sys.argv[2]
        if doc:
            if doc_type.lower() == 'epytext':
                tup = epytext(doc)
            elif doc_type.lower() == 'sphinx':
                tup = sphinx(doc)
            elif doc_type.lower() == 'numpy':
                tup = numpy(doc)
            else:
                tup = google(doc)
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
        """
        Visits a class definition node and adds type annotations.

        This method analyzes the attributes of a class based on the information from the docstring, and modifies the AST node to include the appropriate type annotations.

        Args:
            node (ast.FunctionDef): The function definition node to process.

        Returns:
            ast.ClassDef: The potentially modified class definition node with updated type annotations.
        """
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
    """Entry point for the script. Parses arguments and runs the main workflow."""
    try:
        filepath = sys.argv[1]
        doc_type = sys.argv[2]
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

        print(new_code)

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except IndexError:
        print("Error: Please provide a file path and docstring type as command line arguments.")

if __name__ == '__main__':
    main()
