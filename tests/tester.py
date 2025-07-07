import sys
import importlib

def findbase(cls, visited=None):
    if visited is None:
        visited = set()

    for base in cls.__bases__:
        if base not in visited:
            print(base)
        if base is not object:
            findbase(base, visited)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 tester.py <filename> <classname>")
        sys.exit(1)

    arg1 = sys.argv[1]
    filename = arg1[:len(arg1) - 3]
    #print(filename)
    classname = sys.argv[2]
    
    try:
        module = importlib.import_module(filename)
        cls = getattr(module, classname)
        findbase(cls)
    except ModuleNotFoundError:
        print(f"Error: Module '{filename}' not found.")
    except AttributeError:
        print(f"Error: Class '{classname}' not found in module '{filename}'.")


if __name__ == "__main__":
    main()
