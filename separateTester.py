import ast
from pprint import pprint
import sys
from pathlib import Path
import builtins

print(ast.dump(ast.parse("""\
from lib import D as DEE
"""), indent=4))

#pprint(sys.path)
#pprint(Path.cwd())
#pprint(builtins)