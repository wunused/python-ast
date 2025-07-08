import sys
from pprint import pprint
from anytree import Node

class someClass(Node):
    def somefunction():
        pass
pprint(sys.path)
print(sys.prefix != sys.base_prefix)