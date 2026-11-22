"""Решение систем, невязки, оценка памяти, бенчмарки."""

import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve


def residual_metrics(matrix, solution, rhs):
    """Абсолютная и относительная невязки: ||Ax-b|| и ||Ax-b||/||b||."""
    r = matrix @ solution - rhs
    abs_res = float(np.linalg.norm(r))
    rel_res = abs_res / float(np.linalg.norm(rhs)) if np.linalg.norm(rhs) else abs_res
    return abs_res, rel_res


def solve_dense(matrix, rhs):
    """Решение плотной системы через numpy.linalg.solve."""
    return np.linalg.solve(matrix, rhs)


def solve_sparse(matrix, rhs):
    """Решение CSR-системы через scipy.sparse.linalg.spsolve."""
    return spsolve(matrix, rhs)


def dense_memory_bytes(n):
    """Теоретический объём плотного хранения (float64): 8*n^2 байт."""
    return 8 * n * n


def csr_memory_bytes(matrix):
    """Фактический объём хранения CSR: data + indices + indptr (в байтах)."""
    m = matrix.tocsr()
    return int(m.data.nbytes + m.indices.nbytes + m.indptr.nbytes)


def _median_time(fn, repeats):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return float(np.median(times))


def benchmark_variant(alpha, f, sizes, dense_limit=320, repeats=3):
    """Прогнать серию размеров и вернуть список словарей с метриками.

    Для N <= dense_limit строится и решается плотная система,
    для всех N строится и решается CSR-система.
    Печать и графики внутри не выполняются — только возврат данных.
    """
    from .matrices import build_rhs, build_dense_matrix, build_sparse_matrix

    rows = []
    for n in sizes:
        x, b = build_rhs(n, f)

        # --- CSR ---
        t0 = time.perf_counter()
        A_csr = build_sparse_matrix(n, alpha)
        t_build_csr = time.perf_counter() - t0

        t_solve_csr = _median_time(lambda: solve_sparse(A_csr, b), repeats)
        u_csr = solve_sparse(A_csr, b)
        abs_csr, rel_csr = residual_metrics(A_csr, u_csr, b)
        mem_csr = csr_memory_bytes(A_csr)
        nnz = int(A_csr.nnz)

        row = {
            "N": n,
            "nnz": nnz,
            "method": "CSR",
            "build_time_s": t_build_csr,
            "solve_time_s": t_solve_csr,
            "abs_residual": abs_csr,
            "rel_residual": rel_csr,
            "memory_bytes": mem_csr,
            "memory_MB": mem_csr / 1024**2,
        }

        # --- Dense (только в безопасных пределах) ---
        if n <= dense_limit:
            t0 = time.perf_counter()
            A_dense = build_dense_matrix(n, alpha)
            t_build_dense = time.perf_counter() - t0

            t_solve_dense = _median_time(lambda: solve_dense(A_dense, b), repeats)
            u_dense = solve_dense(A_dense, b)
            abs_d, rel_d = residual_metrics(A_dense, u_dense, b)
            mem_dense = dense_memory_bytes(n)

            row.update({
                "dense_build_time_s": t_build_dense,
                "dense_solve_time_s": t_solve_dense,
                "dense_abs_residual": abs_d,
                "dense_rel_residual": rel_d,
                "dense_memory_MB": mem_dense / 1024**2,
            })
        else:
            # Теоретическая память плотного хранения (не создаём матрицу)
            row.update({
                "dense_build_time_s": None,
                "dense_solve_time_s": None,
                "dense_abs_residual": None,
                "dense_rel_residual": None,
                "dense_memory_MB": dense_memory_bytes(n) / 1024**2,
            })

        rows.append(row)

    return rows