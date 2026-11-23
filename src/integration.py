import numpy as np
from scipy.integrate import quad


def scipy_quad(g, a, b, *, epsabs, epsrel):
    """Адаптивное интегрирование. Возврат: (value, error_estimate)."""
    val, err = quad(g, a, b, epsabs=epsabs, epsrel=epsrel)
    return float(val), float(err)


def composite_trapezoid(g, a, b, n):
    """Составная формула трапеций с n отрезками."""
    if n < 1:
        raise ValueError("n должно быть >= 1")
    x = np.linspace(a, b, n + 1)
    y = g(x)
    h = (b - a) / n
    return float(h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1]))


def compare_integrals(Tn, quad_val, quad_err, exact_integral):
    """Сравнение Tn с quad и (если есть) с точным значением."""
    out = {
        "method_difference": abs(Tn - quad_val),   # |Tn - quad|
        "quad_error":        quad_err,
    }
    if exact_integral:
        out["actual_error_Tn"]    = abs(Tn - exact_integral)
        out["actual_error_quad"]  = abs(quad_val - exact_integral)
    return out