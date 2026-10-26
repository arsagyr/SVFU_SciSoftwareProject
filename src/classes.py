 
from numpy import linspace, argmin, argmax, trapezoid
from sympy import symbols, pi, E, sqrt, sin, cos, tan, exp, log, Abs
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)
from sympy.core.sympify import SympifyError

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)
 
SAFE_BOUNDS = {
    "pi": pi, "E": E, "e": E, "tau": 2 * pi,
    "sqrt": sqrt, "exp": exp, "log": log, "Abs": Abs,
    "sin": sin, "cos": cos, "tan": tan,
}

def calc(value: float, expr_str: str, var: str = 'x') -> float:
    symbol = symbols(var)
    expr = parse_expr(expr_str, transformations=standard_transformations + (implicit_multiplication_application,),
                      local_dict={var: symbol})
    return float(expr.subs(symbol, value).evalf())

@staticmethod
def parse_bound(value, name: str = "граница") -> float:
    """
    Преобразует строку или число в float.

    Принимает:
        - числа: 0, 3.14, -2
        - строки-числа: "0", "3.14", "-2"
        - выражения SymPy: "pi", "pi/2", "2*pi", "sqrt(2)", "sqrt(3)/2"
    """
    if isinstance(value, (int, float)):
        result = float(value)
        if result != result or result in (float("inf"), float("-inf")):
            raise ValueError(f"{name}: значение должно быть конечным числом")
        return result
 
    s = str(value).strip()
    if not s:
        raise ValueError(f"{name}: пустая строка")
    try:
        result = float(s)
        if result != result or result in (float("inf"), float("-inf")):
            raise ValueError(f"{name}: значение должно быть конечным числом")
        return result
    except ValueError:
        pass   # не число — пробуем как выражение SymPy
 
    try:
        expr = parse_expr(
            s,
            transformations=TRANSFORMATIONS,
            local_dict=SAFE_BOUNDS,
            global_dict={"__builtins__": {}},   # запрет встроенных Python
        )
    except (SympifyError, SyntaxError, TypeError) as e:
        raise ValueError(f"{name}: не удалось разобрать '{s}': {e}") from e
 
    try:
        numeric = expr.evalf()
    except Exception as e:
        raise ValueError(f"{name}: ошибка вычисления '{s}': {e}") from e

    if numeric.is_real is False:
        raise ValueError(f"{name}: результат '{s}' — комплексное число: {numeric}")
    if numeric in (float("nan"), float("inf"), float("-inf")):
        raise ValueError(f"{name}: результат '{s}' не определён: {numeric}")

    return float(numeric)

class Whole_Domain:
    formula = str()
    min_x = None
    max_x = None
    metrics = None
    def __init__(self, min_x : float = 0.0, max_x: float = 1.0, formula : str = 'y = x'):
        self.formula = formula
        self.min_x = min_x
        self.max_x = max_x

    def set_formula(self, formula : str ):
        try:
            self.formula = formula
        except ValueError:
            raise ValueError("Неверный формат формулы")
        

    def make_data(self, start, end, n):
        try:
            self.min_x = start
        except ValueError:
            raise ValueError("Неверный формат левой границы. Ожидается число.")
        try:
            self.max_x = end
        except ValueError:
            raise ValueError("Неверный формат правой границы. Ожидается число")
        try:
            n = int(n)
        except ValueError:
            raise ValueError("Неверный формат n. Ожидается целое число.")
        if self.min_x > self.max_x:
            raise ValueError("Значение левой границы не может быть больше правой")
        if n < 2:
            raise ValueError("n должно быть не меньше 2")
        x, y = [], []
        step = (self.max_x - self.min_x) / n
        xi = self.min_x
        i = 0
        for i in range(n):
            try:
                yi = calc(xi, self.formula) 
            except:
                print("Ошибка в чтении формулы")
            x.append(xi)
            y.append(yi)
            xi += step
        return x, y

    def calculate_metrics(self):
        if self.min_x and self.max_x:
            self.metrics = calculate_metrics(make_data(self.min_x, self.max_x))
        else:
            print("Не указаны границы")

