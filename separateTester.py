import ast

print(ast.dump(ast.parse("""\
def f(self, a: annotation, b, c, d, e, f = 2, g = 3):
    pass
"""), indent=4))