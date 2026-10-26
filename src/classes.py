 
from numpy import linspace, argmin, argmax, trapezoid
from sympy import symbols, pi, E, sqrt, sin, cos, tan, exp, log, Abs
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)
from sympy.core.sympify import SympifyError

from src.calculations import calc, calculate_metrics, make_data

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
        

    def make_data(self, n: int):
        return make_data(start=self.min_x, end=self.max_x, n=n, formula=self.formula)

    def calculate_metrics(self, x, y):
        if (self.min_x != None) and (self.max_x != None):
            self.metrics = calculate_metrics(x, y)
        else:
            print("Не указаны границы")
        return self.metrics

