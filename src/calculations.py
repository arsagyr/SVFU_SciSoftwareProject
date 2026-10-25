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
from src.classes import Whole_Domain
import numpy as np

# calculations.py

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
        # "Среднее":     float(np.mean(y)),
        # "Минимум":      float(np.min(y)),
        # "Максимум":      float(np.max(y)),
        # "Стандартное отклонение":      float(np.std(y)),
        # "Координаты минимума": (float(x[i_min]), float(y[i_min])),
        # "координаты максимума": (float(x[i_max]), float(y[i_max])),
        # "Интеграл": float(np.trapezoid(y, x)),  