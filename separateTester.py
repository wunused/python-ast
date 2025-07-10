import ast
from pprint import pprint
import sys
from pathlib import Path
import builtins
from types import MethodDescriptorType

print(ast.dump(ast.parse("""\
class someclass(object):
    pass
"""), indent=4))

pprint(sys.path)
#pprint(Path.cwd())
#pprint(builtins)
pprint(tuple.__dict__)

class myTuple(tuple):
    y = 3
    
    def someFunc():
        z = 7
        print(z)
    
    x = y+2
    pass

x = myTuple()
pprint(myTuple.__mro__)
pprint(myTuple.__dict__)
pprint(myTuple.__bases__)
class myTuple2(myTuple):
    pass
pprint(myTuple2.__bases__)
pprint(myTuple2.__mro__)
pprint(myTuple2.__dict__)
pprint(myTuple().someFunc.__dict__)
pprint(object.__dict__)

print(x.__sizeof__())

for k, v in object.__dict__.items():
    if isinstance(v, MethodDescriptorType):
        
        print(k)
        
        print(type(v))