"""Методы решения нелинейных уравнений: бисекция и Brentq."""

import numpy as np
from scipy.optimize import root_scalar


def bisection(f, a, b, *, xtol, rtol, max_iter):
    """Метод бисекции. Возврат: (root, residual, iterations, converged)."""
    if a >= b:
        raise ValueError("Требуется a < b")
    if not (np.isfinite(a) and np.isfinite(b)):
        raise ValueError("Границы интервала должны быть конечными")

    fa, fb = f(a), f(b)
    if not (np.isfinite(fa) and np.isfinite(fb)):
        raise ValueError("Значения функции на границах должны быть конечными")
    if np.sign(fa) == np.sign(fb):
        raise ValueError("Функция не меняет знак на заданном интервале")

    c, fc = 0.5 * (a + b), f(0.5 * (a + b))
    for it in range(max_iter):
        c = 0.5 * (a + b)
        fc = f(c)
        if abs(b - a) <= xtol + rtol * max(abs(a), abs(b)) or fc == 0.0:
            return c, fc, it, True
        if np.sign(fa) != np.sign(fc):
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c, fc, max_iter, False


def scipy_brentq(f, a, b, *, xtol, rtol, max_iter):
    """Метод Брента (scipy). Возврат: (root, residual, iterations)."""
    res = root_scalar(
        f, bracket=[a, b], method="brentq",
        xtol=xtol, rtol=rtol, maxiter=max_iter,
    )
    root = float(res.root)
    return root, float(f(root)), int(res.iterations)


def compare_roots(root_bis, res_bis, root_brent, res_brent):
    """Сравнение двух приближений.

    res_bis   = (root, residual, iterations)  или (root, residual, iterations, converged)
    res_brent = (root, residual, iterations)
    """
    return {
        "difference_roots":     abs(root_bis - root_brent),
        "residual_bisection":   abs(res_bis[1]),
        "residual_brentq":      abs(res_brent[1]),
        "iterations_bisection": res_bis[2],
        "iterations_brentq":    res_brent[2],
    }