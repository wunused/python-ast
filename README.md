# python-ast
This is a repository of tools/applications used to analyze and modify python code into a standard format. 

## class_hierarchy_analyzer
This folder contains class hierarchy analyzer code (cha.py) that analyzes a given file and returns the inheritance tree of the file.
This folder also contains test cases for the analyzer.
### test_module.py
This is a pytest file that automatically tests the analyzer with all the test cases when run.
### tests/tester.py
This file dynamically analyzes class hierarchy with python.

## docstring_parser
This folder contains docstring parsing code (dsp.py) that processes an input file and outputs to stdout modified code with type annotations based on the docstring.
This folder also contains test cases for the parser.
### test_docstring.py
This is a pytest file that automatically tests the parser with all the tests cases when run.
