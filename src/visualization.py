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

def save_all(
    out_dir: str | Path,
    variant: Variant,
    X: np.ndarray,
    Y: np.ndarray,
    U: np.ndarray,
    mask: np.ndarray,
    summary: Dict[str, float],
    bench_rows: List[BenchRow],
    reports: Dict[Tuple[int, int], ValidationReport] | None = None,
) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
 
    np.savez_compressed(
        out / "field_data.npz",
        X=X, Y=Y, U=U, mask=mask.astype(np.uint8),
        variant_number=variant.number, variant_name=variant.name,
    )
 
    payload = {
        "variant": asdict(variant),
        "stats": summary,
    }
    if reports is not None:
        payload["validation"] = {
            f"{ny}x{nx}": asdict(rep) for (nx, ny), rep in reports.items()
        }
    with open(out / "summary.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
 
    with open(out / "benchmark.csv", "w", encoding="utf-8") as f:
        f.write("ny,nx,t_loop_s,t_numpy_s,speedup\n")
        for r in bench_rows:
            f.write(f"{r.ny},{r.nx},{r.t_loop:.6f},{r.t_numpy:.6f},{r.speedup:.2f}\n")

 
    fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=120)
    im = ax.pcolormesh(X, Y, np.where(mask, U, np.nan),
                       shading="auto", cmap="viridis")
    ax.contour(X, Y, mask.astype(float), levels=[0.5], colors="w", linewidths=0.8)
    ax.set_title(f"u(x,y) = {variant.name}\nmask: {variant.mask_condition}")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_aspect("equal")
    fig.colorbar(im, ax=ax, label="u")
    fig.tight_layout()
    fig.savefig(out / "field.png")
    plt.close(fig)