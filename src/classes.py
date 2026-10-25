# make_data(start, end, n)
# - проверить, что end > start и n >= 50
# - создать массив x из n точек
# - вычислить y по формуле варианта
# - вернуть массивы x и y

# calculate_metrics(x, y)
# - вычислить среднее, минимум, максимум и стандартное отклонение
# - найти координаты минимума и максимума
# - вычислить интеграл методом трапеций
# - вернуть словарь с семью результатами

# Подсказка: используйте linspace, argmin, argmax и trapezoid.
 
from numpy import linspace, argmin, argmax, trapezoid
from sympy import symbols
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

x = symbols('x')

def calc(value: float, expr_str: str, var: str = 'x') -> float:
    symbol = symbols(var)
    expr = parse_expr(expr_str, transformations=standard_transformations + (implicit_multiplication_application,),
                      local_dict={var: symbol})
    return float(expr.subs(symbol, value).evalf())

class Whole_Domain:
    formula = str()
    min_x = float()
    max_x = float()
    metrics = dict()
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
            self.min_x = float(start)
        except ValueError:
            raise ValueError("Неверный формат start. Ожидается число.")
        try:
            self.max_x = float(end)
        except ValueError:
            raise ValueError("Неверный формат end. Ожидается число.")
        try:
            n = int(n)
        except ValueError:
            raise ValueError("Неверный формат n. Ожидается целое число.")
        if self.min_x > self.max_x:
            raise ValueError("Значение start не может быть больше end")

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
        self.metrics()


