import lib
from newApp import pinho

class A(lib.C):
    
	def a_method(self):
		pass
class B(pinho):
    def b_method(self):
        pass
class new(B):
    pass

def main(b, c, d):
    print(b, c, d)

a = A()
