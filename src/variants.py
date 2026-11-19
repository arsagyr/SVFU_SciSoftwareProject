import numpy as np
import math

def get_variant(variant_num):
    """
    Возвращает данные для выбранного варианта.
    Здесь приведен пример для варианта №1. 
    Вам нужно будет заменить функции и интервалы на свои.
    """
    if variant_num == 1:
        # Часть А: xe^x − 1 = 0 [0, 1] 
        f = lambda x: x*math.e**x - 1
        a_root, b_root = 0.0, 1.0
        
        # Часть В: e^(−x) cos(2x) [0, π]
        g = lambda x: np.exp(-x**2)
        a_int, b_int = 0.0, math.pi
        exact_integral = 0.746824132812427
        
        return f, a_root, b_root, g, a_int, b_int, exact_integral
    else:
        raise ValueError("Варианта нет")