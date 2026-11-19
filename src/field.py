from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict, field as dc_field
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


RTOL = 1e-10
ATOL = 1e-12

@dataclass(frozen=True)
class Variant:
    number: int
    name: str
    formula: str                                  
    bounds: Tuple[float, float, float, float]       
    mask_condition: str        
                         
    def evaluate(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        return np.sin(2 * X + Y) + np.cos(X - 2 * Y)

    def mask(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        return (X ** 2 + Y ** 2) <= (np.pi / 2) ** 2


_VARIANTS = {
    6: Variant(
        number=6,
        name="sin(2x+y)+cos(x-2y)",
        formula="np.sin(2*X + Y) + np.cos(X - 2*Y)",
        bounds=(-np.pi, np.pi, -np.pi, np.pi),
        mask_condition="U > 1",
    ),
}


def get_variant(number: int = 6) -> Variant:
    """Вернуть формулу, область и условие маски по номеру варианта."""
    if number not in _VARIANTS:
        raise KeyError(f"Нет варианта {number}. Доступны: {list(_VARIANTS)}")
    return _VARIANTS[number]


 
def make_coordinates(
    bounds: Tuple[float, float, float, float],
    nx: int,
    ny: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, float]:
    """X, Y формы (ny, nx); xc (nx,), yc (ny,); dx, dy."""
    if nx < 1 or ny < 1:
        raise ValueError("nx и ny должны быть >= 1")
    xmin, xmax, ymin, ymax = bounds
    dx = (xmax - xmin) / nx
    dy = (ymax - ymin) / ny
    xc = xmin + (np.arange(nx) + 0.5) * dx
    yc = ymin + (np.arange(ny) + 0.5) * dy
    X = xc[None, :] + np.zeros((ny, 1))
    Y = yc[:, None] + np.zeros((1, nx))
    return X, Y, xc, yc, dx, dy

 
def compute_loop(variant: Variant, xc: np.ndarray, yc: np.ndarray) -> np.ndarray:
    ny, nx = yc.size, xc.size
    U = np.empty((ny, nx), dtype=float)
    for j in range(ny):
        for i in range(nx):
            U[j, i] = variant.evaluate(xc[i], yc[j])
    return U


def compute_numpy(variant: Variant, xc: np.ndarray, yc: np.ndarray) -> np.ndarray:
    X = xc[None, :]
    Y = yc[:, None]
    return variant.evaluate(X, Y)                  # (ny, nx)


 
@dataclass(frozen=True)
class ValidationReport:
    max_abs_diff: float
    mask_area: float
    rect_area: float


def validate_before_bench(
    U_loop: np.ndarray,
    U_np: np.ndarray,
    mask: np.ndarray,
    bounds: Tuple[float, float, float, float],
    *,
    rtol: float = RTOL,
    atol: float = ATOL,
) -> ValidationReport:
    """
    Проверить, что две реализации решают одну и ту же задачу.
    Бросает AssertionError при нарушении любого пункта.
    """
    xmin, xmax, ymin, ymax = bounds
    rect_area = (xmax - xmin) * (ymax - ymin)

    # 1. Форма (ny, nx)
    if U_loop.ndim != 2 or U_np.ndim != 2:
        raise AssertionError(
            f"Поля должны быть 2D: U_loop{U_loop.shape}, U_np{U_np.shape}")
    if U_loop.shape != U_np.shape:
        raise AssertionError(
            f"Формы полей не совпадают: {U_loop.shape} vs {U_np.shape}")

    # 2. Конечность
    if not np.isfinite(U_loop).all():
        raise AssertionError("U_loop содержит нефинитные значения")
    if not np.isfinite(U_np).all():
        raise AssertionError("U_np содержит нефинитные значения")

    # 3. Совпадение с допусками
    max_abs_diff = float(np.max(np.abs(U_loop - U_np)))
    if not np.allclose(U_loop, U_np, rtol=rtol, atol=atol):
        raise AssertionError(
            f"Реализации различаются: max|Δ|={max_abs_diff:.3e} "
            f"(rtol={rtol}, atol={atol})")

    # 4. Маска: bool и та же форма
    if mask.dtype != np.bool_:
        raise AssertionError(f"Маска должна быть bool, получено {mask.dtype}")
    if mask.shape != U_np.shape:
        raise AssertionError(
            f"Форма маски {mask.shape} != формы поля {U_np.shape}")

  
    ny, nx = U_np.shape
    dx = (xmax - xmin) / nx
    dy = (ymax - ymin) / ny
    mask_area = float(mask.sum()) * dx * dy
    if not (0.0 <= mask_area <= rect_area + 1e-12):
        raise AssertionError(
            f"Площадь маски {mask_area:.6f} вне [0, {rect_area:.6f}]")

    return ValidationReport(max_abs_diff, mask_area, rect_area)
 
def analyze_field(
    U: np.ndarray,
    mask: np.ndarray,
    dx: float,
    dy: float,
) -> Dict[str, float]:
    if U.shape != mask.shape:
        raise ValueError(f"Формы U{U.shape} и mask{mask.shape} не совпадают")

    cell_area = dx * dy
    mask_bool = mask.astype(bool)
    n_mask = int(mask_bool.sum())
    n_total = mask_bool.size

    stats: Dict[str, float] = {
        "u_min": float(U.min()),
        "u_max": float(U.max()),
        "u_mean": float(U.mean()),
        "u_std": float(U.std()),
        "mask_fraction": n_mask / n_total,
        "mask_area": n_mask * cell_area,
        "n_cells": n_total,
        "n_mask_cells": n_mask,
        "dx": dx,
        "dy": dy,
    }
    if n_mask:
        u_masked = U[mask_bool]
        stats.update({
            "u_min_masked": float(u_masked.min()),
            "u_max_masked": float(u_masked.max()),
            "u_mean_masked": float(u_masked.mean()),
            "u_std_masked": float(u_masked.std()),
        })
    else:
        stats.update({k: float("nan") for k in (
            "u_min_masked", "u_max_masked", "u_mean_masked", "u_std_masked")})
    return stats


 
@dataclass
class BenchRow:
    nx: int
    ny: int
    t_loop: float
    t_numpy: float
    speedup: float


def benchmark(
    variant: Variant,
    sizes: Iterable[Tuple[int, int]] = ((50, 50), (200, 200), (500, 500)),
    repeats: int = 1,
    *,
    rtol: float = RTOL,
    atol: float = ATOL,
) -> Tuple[List[BenchRow], Dict[str, object], Dict[Tuple[int, int], ValidationReport]]:
    rows: List[BenchRow] = []
    reports: Dict[Tuple[int, int], ValidationReport] = {}
    results: Dict[str, object] = {}

    for nx, ny in sizes:
        _, _, xc, yc, dx, dy = make_coordinates(variant.bounds, nx, ny)
        U_loop = compute_loop(variant, xc, yc)
        U_np = compute_numpy(variant, xc, yc)

        X = xc[None, :] + np.zeros((ny, 1))
        Y = yc[:, None] + np.zeros((1, nx))
        mask = variant.mask(X, Y)

        # --- валидация ДО замеров ---
        report = validate_before_bench(U_loop, U_np, mask,
                                       variant.bounds, rtol=rtol, atol=atol)
        reports[(nx, ny)] = report
        print(f"[validate] ny={ny:<4} nx={nx:<4}  "
              f"max|Δ|={report.max_abs_diff:.2e}  "
              f"mask_area={report.mask_area:.3f}/{report.rect_area:.3f}")

        # --- замеры ---
        _ = compute_numpy(variant, xc, yc)                     # прогрев

        t0 = time.perf_counter()
        for _ in range(repeats):
            compute_loop(variant, xc, yc)
        t_loop = (time.perf_counter() - t0) / repeats

        t0 = time.perf_counter()
        for _ in range(repeats):
            compute_numpy(variant, xc, yc)
        t_numpy = (time.perf_counter() - t0) / repeats

        rows.append(BenchRow(nx, ny, t_loop, t_numpy, t_loop / t_numpy))
        results = {"xc": xc, "yc": yc, "dx": dx, "dy": dy,
                   "X": X, "Y": Y, "U": U_np, "U_loop": U_loop, "mask": mask}
        print(f"[bench   ] ny={ny:<4} nx={nx:<4}  "
              f"loop={t_loop*1e3:8.2f} ms  numpy={t_numpy*1e3:8.3f} ms  "
              f"x{t_loop/t_numpy:6.1f}")

    return rows, results, reports

