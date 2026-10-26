import numpy as np
from sympy import symbols, pi, E, sqrt, sin, cos, tan, exp, log, Abs, sympify, Integer, Float
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)

from sympy import symbols, pi, E, sqrt, sin, cos, tan, exp, log, Abs, tanh, sinh, cosh

SAFE_LOCALS = {
    # константы
    "pi":  pi,
    "E":   E,
    "e":   E,
    "tau": 2 * pi,
    # функции
    "sqrt": sqrt,
    "sin":  sin,
    "cos":  cos,
    "tan":  tan,
    "tanh": tanh,   # <-- добавили для 5-й формулы
    "sinh": sinh,
    "cosh": cosh,
    "exp":  exp,
    "log":  log,
    "Abs":  Abs,
}

SAFE_BOUNDS = {
    "pi": pi, "E": E, "e": E, "tau": 2 * pi,
    "sqrt": sqrt, "exp": exp, "log": log, "Abs": Abs,
    "sin": sin, "cos": cos, "tan": tan,
}

METRIC_LABELS = {
    "mean":      "Среднее значение",
    "min":       "Минимум",
    "max":       "Максимум",
    "std":       "Стандартное отклонение",
    "min_point": "Точка минимума",
    "max_point": "Точка максимума",
    "integral":  "Интеграл (метод трапеций)",
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


def calc(value: float, expr_str: str, var: str = 'x') -> float:
    symbol = symbols(var)
    expr = parse_expr(expr_str, transformations=TRANSFORMATIONS,
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


def make_data(start, end, n, formula):
    try:
        n = int(n)
    except ValueError:
        raise ValueError("Неверный формат n. Ожидается целое число.")
    if start > end:
        raise ValueError("Значение левой границы не может быть больше правой")
    if n < 2:
        raise ValueError("n должно быть не меньше 2")
    x, y = [], []
    step = (end - start) / n
    xi = start
    i = 0
    for i in range(n):
        try:
            yi = calc(xi, formula) 
        except:
            print("Ошибка в чтении формулы")
        x.append(xi)
        y.append(yi)
        xi += step
    return x, y


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

