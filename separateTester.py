import ast
from pprint import pprint
import sys
from pathlib import Path
import builtins

"""print(ast.dump(ast.parse("""\
"""def f(self, a: annotation, b, c, d, e, f = 2, g = 3):
    pass"""
"""), indent=4))"""

#pprint(sys.path)
#pprint(Path.cwd())
pprint(builtins)