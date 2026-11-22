import numpy as np
import math

def get_variant(variant_num):
    if variant_num == 6:
        # Часть А: xe^x − 1 = 0 [0, 1] 
        f = lambda x: x*math.e**x - 1  
        a_root, b_root = 0.0, 1.0
        
        # Часть В: e^(−x) cos(2x) [0, π]
        g = lambda x: np.exp(-x**2)
        a_int, b_int = 0.0, math.pi
        # Неопределённый интеграл e^(−x)*cos(2x) равен (2in2x - cos2x)/5 * e^(−x) 
        exact_integral = 0.382714432694
        
        return f, a_root, b_root, g, a_int, b_int, exact_integral
    else:
        raise ValueError("Варианта нет")