"""Данные вариантов: уравнение f(x)=0, функция g(x), точный интеграл."""

import numpy as np


def get_variant(variant_num: int):
    """Вернуть (f, a_root, b_root, g, a_int, b_int, exact_integral)."""
    if variant_num != 6:
        raise ValueError(f"Вариант {variant_num} не поддерживается")

    # Часть А: x * e^x - 1 = 0,  x ∈ [0, 1]
    f = lambda x: x * np.exp(x) - 1.0
    a_root, b_root = 0.0, 1.0

    # Часть В: g(x) = e^(-x) * cos(2x),  x ∈ [0, π]
    g = lambda x: np.exp(-x) * np.cos(2.0 * x)
    a_int, b_int = 0.0, np.pi

    # ∫ e^(-x) cos(2x) dx = e^(-x)(2 sin 2x - cos 2x) / 5
    def G(x):
        return np.exp(-x) * (2.0 * np.sin(2.0 * x) - np.cos(2.0 * x)) / 5.0

    exact_integral = 0.1913648067

    return f, a_root, b_root, g, a_int, b_int, exact_integral