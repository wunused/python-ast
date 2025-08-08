import ast
import docstring_parser
import sys

def google(doc):
    """
    Parses through the docstring and finds type information based on keywords in the function's Google Style Docstring

    Args:
        doc (str): the function's docstring

    Returns:
        array: an array where the first value is a dictionary of the function's arguments and the second value is the return type specified in the docstring
    """
    parsed = docstring_parser.parse(doc, style=docstring_parser.DocstringStyle.GOOGLE)

    tup = []
    dictionary = {param.arg_name: param.type_name for param in parsed.params}
    return_type = parsed.returns.type_name if parsed.returns else None
    tup.append(dictionary)
    tup.append(return_type)
    return tup

def sphinx(doc):
    """
    Parses through the docstring and finds type information based on keywords in the function's Sphinx Style Docstring

    Args:
       doc (str): the function's docstring

    Returns:
        array: an array where the first value is a dictionary of the function's arguments and the second value is the return type specified in the docstring
    """
    parsed = docstring_parser.parse(doc, style=docstring_parser.DocstringStyle.REST)
    tup = []
    dictionary = {param.arg_name: param.type_name for param in parsed.params}
    return_type = parsed.returns.type_name if parsed.returns else None
    tup.append(dictionary)
    tup.append(return_type)
    return tup

def numpy(doc):
    """
    Parses through the docstring and finds type information based on keywords in the function's NumPy Style Docstring

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
#    parsed = docstring_parser.parse(doc, style=docstring_parser.DocstringStyle.NUMPY)
#    tup = []
#    dictionary = {param.arg_name: param.type_name for param in parsed.params}
#    return_type = parsed.returns.type_name if parsed.returns else None
#    tup.append(dictionary)
#    tup.append(return_type)
#    return tup

def epytext(doc):
    """
    Parses through the docstring and finds type information based on keywords in the function's Epytext Style Docstring

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

def google_class(doc):
    """
    Parses through the docstring and finds type information based on keywords in the class's Google Style Docstring

    Args:
       doc (str): the class's docstring

    Returns:
       dictionary: a dictionary of the attributes of the class
    """
    dictionary = {}
    attr = False
    parts = doc.strip().splitlines()
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        if "Attributes" in part:
            attr = True
        elif attr:
            param = part.strip().split(" ")
            length = len(param)
            key = param[0]
            val = param[1][1:len(param[1])-2]
            dictionary[key] = val
    return dictionary

def sphinx_class(doc):
    """
    Parses through the docstring and finds type information based on keywords in the class's Sphinx Style Docstring

    Args:
       doc (str): the class's docstring

    Returns:
       dictionary: a dictionary of the attributes of the class
    """
    dictionary = {}
    parts = doc.strip().splitlines()
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        if ":vartype" in part:
            param = part.strip().split(" ")
            length = len(param)
            key = param[length-2][:len(param[length-2])-1]
            val = param[length-1]
            dictionary[key] = val
    return dictionary

def numpy_class(doc):
    """
    Parses through the docstring and finds type information based on keywords in the class's NumPy Style Docstring

    Args:
       doc (str): the class's docstring

    Returns:
       dictionary: a dictionary of the attributes of the class
    """
    dictionary = {}
    attr = False
    parts = doc.strip().splitlines()
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        if "Attributes" in part:
            attr = True
        elif attr and ':' in part:
            if '-' in part:
                continue
            param = part.strip().split(" ")
            key = param[0]
            val = param[2]
            dictionary[key] = val
    return dictionary


def epytext_class(doc):
    """
    Parses through the docstring and finds type information based on keywords in the class's Epytext Style Docstring

    Args:
       doc (str): the class's docstring

    Returns:
       dictionary: a dictionary of the attributes of the class
    """
    dictionary = {}
    parts = doc.strip().splitlines()
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        if "@type" in part:
            param = part.strip().split(" ")
            key = param[0][:len(param[0])-1]
            val = param[1]
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
        doc_type = sys.argv[2]
        if doc: 
            if doc_type == 'sphinx':
                dictionary = sphinx_class(doc)
            elif doc_type == 'numpy':
                dictionary = numpy_class(doc)
            elif doc_type == 'epytext':
                dictionary == epytext_class(doc)
            else:
                dictionary = google_class(doc)
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
