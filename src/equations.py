import numpy as np
from scipy.optimize import root_scalar

def bisection(f, a, b, *, xtol, rtol, max_iter):
    """
    Реализация метода бисекции.
    Остановка по ширине интервала: |b - a| <= xtol + rtol * max(|a|, |b|)
    """
    if a >= b:
        raise ValueError("Требуется a < b")
    if not (np.isfinite(a) and np.isfinite(b)):
        raise ValueError("Границы интервала должны быть конечными числами")
    
    fa = f(a)
    fb = f(b)
    if not (np.isfinite(fa) and np.isfinite(fb)):
        raise ValueError("Значения функции на границах должны быть конечными")
    if fa * fb > 0:
        raise ValueError("Функция не меняет знак на заданном интервале")

    iter_count = 0
    c = a
    fc = fa
    
    while iter_count < max_iter:
        c = (a + b) / 2.0
        fc = f(c)
        
        # Проверка сходимости по ширине интервала
        if abs(b - a) <= xtol + rtol * max(abs(a), abs(b)):
            return c, fc, iter_count, True
            
        if fc == 0:
            return c, fc, iter_count, True
            
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
            
        iter_count += 1

    # Если превышено число итераций
    return c, fc, iter_count, False

def scipy_brentq(f, a, b, *, xtol, rtol, max_iter):
    """
    Обертка над scipy.optimize.root_scalar с методом brentq.
    """
    res = root_scalar(
        f, 
        bracket=[a, b], 
        method='brentq', 
        xtol=xtol, 
        rtol=rtol, 
        maxiter=max_iter
    )
    # Возвращаем корень, невязку, число итераций
    return res.root, f(res.root), res.iterations

def compare_roots(root_bis, res_bis, root_brent, res_brent):
    """
    Сравнение результатов двух методов.
    res_bis и res_brent - кортежи (root, residual, iter_count)
    """
    diff = abs(root_bis - root_brent)
    return {
        "difference_roots": diff,
        "residual_bisection": abs(res_bis[1]),
        "residual_brentq": abs(res_brent[1]),
        "iterations_bisection": res_bis[2],
        "iterations_brentq": res_brent[2]
    }