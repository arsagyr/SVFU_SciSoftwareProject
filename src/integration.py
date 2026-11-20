import numpy as np
from scipy.integrate import quad

def composite_trapezoid(g, a, b, n):
    if n <= 0:
        raise ValueError("Число отрезков n должно быть натуральным")
    
    x = np.linspace(a, b, n + 1)
    y = g(x)

    if np.any(~np.isfinite(y)):
        raise ValueError("Функция содержит некорректные значения (inf/nan) на интервале")
    h = (b - a) / n
    integral = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral

def scipy_quad(g, a, b, *, epsabs, epsrel):
    val, err = quad(g, a, b, epsabs=epsabs, epsrel=epsrel)
    return val, err

def compare_integrals(Tn, quad_val, quad_err, exact_val=None):
    result = {
        "method_difference": abs(Tn - quad_val),
        "quad_estimate_error": quad_err
    }
    if exact_val is not None:
        result["actual_error_Tn"] = abs(Tn - exact_val)
        if not np.isclose(exact_val, 0):
            result["relative_error_Tn"] = abs(Tn - exact_val) / abs(exact_val)
    return result