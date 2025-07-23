import sys

def main():
    try:
        file_path = sys.argv[1]
        with open(file_path, 'r') as f:
            deftype = ""
            name = ""
            my_docstring = []
            for line in f:
                if line.strip():
                    # print("LINES PARSING:", line)
                    if 'def' in line:
                        # print("Found def!")
                        deftype = "def"
                        line = line.strip()
                        parts = line.split(" ")
                        findname = parts[1].split("(")
                        name = findname[0]
                    elif 'class' in line:
                        # print("Found class!")
                        deftype = "class"
                    elif deftype:
                        if my_docstring:
                            if '"""' in line or "'''" in line:
                                my_docstring.append('"')
                                docstring = ''.join(my_docstring)
                                if deftype == "def":
                                    print(f"function definition `{name}`:", docstring)
                                else:
                                    print(f"class definition `{name}`:", docstring)
                                deftype = ""
                                name = ""
                                my_docstring = []
                            else:
                                my_docstring.append(line.strip())
                        else:
                            #limits docstring to the first nonempty line after def
                            if '"""' in line or "'''" in line:
                                my_docstring.append('"')
                            else:
                                deftype = ""
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except IndexError:
        print("Error: Please provide a file path as a command-line argument.")

if __name__ == '__main__':
    main()
