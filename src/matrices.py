"""Построение правой части и матриц системы (плотной и CSR)."""

import numpy as np
import scipy.sparse as sp


def _validate(n, alpha):
    if n < 2:
        raise ValueError(f"n должно быть >= 2, получено {n}")
    if alpha <= 0:
        raise ValueError(f"alpha должно быть > 0, получено {alpha}")


def build_rhs(n, f):
    """Вернуть x (узлы) и одномерный вектор b длины n.

    x_i = i / (n + 1), i = 1..n
    b_i = f(x_i)
    """
    _validate(n, 1.0)
    x = np.arange(1, n + 1, dtype=float) / (n + 1)
    b = np.asarray(f(x), dtype=float)
    if b.shape != (n,):
        raise ValueError(f"f вернула форму {b.shape}, ожидалась ({n},)")
    if not np.all(np.isfinite(b)):
        raise ValueError("Правая часть содержит нефинитные значения")
    return x, b


def build_dense_matrix(n, alpha):
    """Вернуть плотную ndarray формы (n, n).

    Трёхдиагональная матрица:
        diag   = 2 + alpha
        off    = -1
    (стандартная конечно-разностная аппроксимация -u'' + alpha*u = f)
    """
    _validate(n, alpha)
    A = np.zeros((n, n), dtype=float)
    idx = np.arange(n)
    A[idx, idx] = 2.0 + alpha
    if n > 1:
        A[idx[:-1], idx[:-1] + 1] = -1.0
        A[idx[1:], idx[1:] - 1] = -1.0
    return A


def build_sparse_matrix(n, alpha):
    """Вернуть CSR sparse array формы (n, n).

    nnz = 3n - 2 (для n >= 2).
    """
    _validate(n, alpha)
    main = np.full(n, 2.0 + alpha)
    off = np.full(n - 1, -1.0)
    A = sp.diags(
        diagonals=[main, off, off],
        offsets=[0, 1, -1],
        shape=(n, n),
        format="csr",
    )
    return A