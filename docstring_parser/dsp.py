import ast
import sys

def main():
    try:
        filepath = sys.argv[1]
        with open(filepath, 'r') as f:
            code_content = f.read()
        tree = ast.parse(code_content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node)
                if doc:
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
