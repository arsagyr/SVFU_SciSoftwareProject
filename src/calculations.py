from src.classes import Whole_Domain
import numpy as np

from sympy import symbols, pi, E, sqrt, sin, cos, tan, exp, log, Abs, sympify, Integer, Float
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)

SAFE_LOCALS = {
    "pi":  pi,
    "E":   E,
    "e":   E,
    "tau": 2 * pi,
    "sqrt": sqrt,
    "sin":  sin,
    "cos":  cos,
    "tan":  tan,
    "exp":  exp,
    "log":  log,
    "Abs":  Abs,
}


def parse_value(s, name: str = "значение") -> float:
    """Строка или число → float. Понимает pi, sqrt(2), 2*pi, 3.14."""
    # число
    if isinstance(s, (int, float)):
        return float(s)

    text = str(s).strip()
    if not text:
        raise ValueError(f"{name}: пустая строка")

    # обычное число
    try:
        return float(text)
    except ValueError:
        pass

    # выражение SymPy
    try:
        expr = parse_expr(text, transformations=TRANSFORMATIONS,
                          local_dict=SAFE_LOCALS,
                                  global_dict={
                                    "__builtins__": {},
                                    "Integer": Integer,
                                    "Float": Float,
                                }
                          )
    except Exception as e:
        raise ValueError(f"{name}: не удалось разобрать '{text}': {e}") from e

    if expr.free_symbols:
        raise ValueError(f"{name}: в выражении '{text}' есть переменные")
    try:
        return float(expr)
    except Exception as e:
        raise ValueError(f"{name}: не удалось вычислить '{text}': {e}") from e


# from sympy import symbols, N, pi, E
# from sympy.parsing.sympy_parser import (
#     parse_expr, standard_transformations, implicit_multiplication_application
# )

# transformations = standard_transformations + (implicit_multiplication_application,)
# x = symbols("x")

# CONSTANTS = {
#     "pi":  pi,
#     "E":   E,
#     "e":   E,
#     "tau": 2 * pi,
# }

# def parse_value(s: str) -> float:
#     """Принимает '3.14', 'pi/2', '2*pi', 'sqrt(2)' — возвращает float."""
#     local = {**CONSTANTS, "x": x}
#     expr = parse_expr(str(s), transformations=transformations, local_dict=local)
#     return float(expr.evalf())
 

METRIC_LABELS = {
    "mean":      "Среднее значение",
    "min":       "Минимум",
    "max":       "Максимум",
    "std":       "Стандартное отклонение",
    "min_point": "Точка минимума",
    "max_point": "Точка максимума",
    "integral":  "Интеграл (метод трапеций)",
}

domain = Whole_Domain(formula = 'x')

def make_data(start, end, n):
    return domain.make_data(start, end, n)

def calculate_metrics(x, y) -> dict:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    i_min = np.argmin(y)
    i_max = np.argmax(y)

    return {
        "mean":     float(np.mean(y)),
        "min":      float(np.min(y)),
        "max":      float(np.max(y)),
        "std":      float(np.std(y)),
        "min_point": (float(x[i_min]), float(y[i_min])),
        "max_point": (float(x[i_max]), float(y[i_max])),
        "integral": float(np.trapezoid(y, x)),  
    }

