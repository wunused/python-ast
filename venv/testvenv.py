import sys
from pprint import pprint
from anytree import Node
from rich._inspect import Inspect


class someClass(Node, Inspect):
    def somefunction():
        pass
pprint(sys.path)
print(sys.prefix != sys.base_prefix)