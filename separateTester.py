import ast

print(ast.dump(ast.parse("""\
@decorator1
@decorator2
def f(a: annotation, b, c, d, e, f = 2, g = 3) -> 'return annotation':
    pass
"""), indent=4))