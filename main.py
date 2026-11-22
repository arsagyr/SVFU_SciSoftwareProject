"""Точка входа: вариант, малые проверки, серия экспериментов, сохранение."""

import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.matrices import build_rhs, build_dense_matrix, build_sparse_matrix
from src.analysis import (
    benchmark_variant, dense_memory_bytes, csr_memory_bytes,
    solve_dense, solve_sparse, residual_metrics,
)

RESULTS = "results"
os.makedirs(RESULTS, exist_ok=True)

# ---- Вариант (измените под себя) ----
VARIANT = {
    1:  (0.10, lambda x: 1.0 + x),
    2:  (0.25, lambda x: np.sin(np.pi * x) + 0.5),
    3:  (0.40, lambda x: np.exp(x) - 1.0),
    4:  (0.60, lambda x: 1.0 + x * (1.0 - x)),
    5:  (0.80, lambda x: 2.0 + np.cos(2 * np.pi * x)),
    6:  (1.00, lambda x: np.exp(-2.0 * x) + x),
    7:  (1.20, lambda x: 1.0 + x**2),
    8:  (1.50, lambda x: 1.2 + x + np.sin(3 * np.pi * x)),
    9:  (1.80, lambda x: (1.0 + x) * np.exp(-x)),
    10: (2.00, lambda x: 0.5 + np.cos(np.pi * x / 2) + x**2),
}
CHOSEN = 4                     # <-- номер варианта
alpha, f = VARIANT[CHOSEN]

# ---- Шаг 1: малое сравнение dense vs CSR ----
N_SMALL = 8
x_s, b_s = build_rhs(N_SMALL, f)
A_d = build_dense_matrix(N_SMALL, alpha)
A_c = build_sparse_matrix(N_SMALL, alpha)

print(f"Вариант {CHOSEN}: alpha = {alpha}")
print(f"N = {N_SMALL}, shape dense = {A_d.shape}, "
      f"shape CSR = {A_c.shape}, nnz = {A_c.nnz}, "
      f"ожидалось nnz = {3*N_SMALL - 2}")

max_diff = float(np.max(np.abs(A_d - A_c.toarray())))
print(f"max |dense - CSR| = {max_diff:.3e}")

u_d = solve_dense(A_d, b_s)
u_c = solve_sparse(A_c, b_s)
print(f"max |u_dense - u_CSR| = {float(np.max(np.abs(u_d - u_c))):.3e}")
print("Невязки dense:", residual_metrics(A_d, u_d, b_s))
print("Невязки CSR  :", residual_metrics(A_c, u_c, b_s))

# ---- Шаг 2: эксперимент ----
SIZES = [80, 160, 320, 1000, 5000, 20000]
rows = benchmark_variant(alpha, f, SIZES, dense_limit=320, repeats=3)

with open(os.path.join(RESULTS, "experiment.json"), "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=2, ensure_ascii=False)

# CSV
import csv
keys = ["N", "nnz", "method", "build_time_s", "solve_time_s",
        "abs_residual", "rel_residual", "memory_MB"]
with open(os.path.join(RESULTS, "experiment.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=keys)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k) for k in keys})

# ---- Шаг 3: график памяти ----
ns = [r["N"] for r in rows]
mem_csr = [r["memory_MB"] for r in rows]
mem_dense = [r["dense_memory_MB"] for r in rows]

plt.figure(figsize=(8, 5))
plt.loglog(ns, mem_dense, "o-", label="Плотная (8·N²)")
plt.loglog(ns, mem_csr, "s-", label="CSR (data+indices+indptr)")
plt.xlabel("N (размер матрицы)")
plt.ylabel("Память, МБ")
plt.title("Зависимость памяти от N")
plt.grid(True, which="both", ls=":")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS, "memory.png"), dpi=150)

# ---- Шаг 4: сводка ----
print("\nN\tnnz\trel_res(CSR)\tmem_CSR,MB\tmem_dense,MB")
for r in rows:
    print(f"{r['N']}\t{r['nnz']}\t{r['rel_residual']:.3e}\t"
          f"{r['memory_MB']:.3e}\t{r['dense_memory_MB']:.3e}")

print("\nГотово: results/experiment.csv, results/experiment.json, results/memory.png")