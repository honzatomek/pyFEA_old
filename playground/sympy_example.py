from sympy import *
import matplotlib


if __name__ == '__main__':
    x, y, z = symbols('x y z')
    init_printing()
    expr = 2 * x ** 2 - 3 * x + 1
    pprint(factor(expr), use_unicode=True)
    print(str(expr))
    expr = 1 / x
    pprint(expr)
    pprint(expr, use_unicode=False)
