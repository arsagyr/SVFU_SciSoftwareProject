from src.field import *
from src.visualization import *

def main() -> int:
    variant = get_variant(6)

    # --- бенчмарк (внутри валидация ДО замеров) ---
    try:
        rows, res, reports = benchmark(
            variant,
            sizes=((50, 50), (200, 200), (500, 500)),
            repeats=1,
        )
    except AssertionError as e:
        print(f"[STOP] Валидация не пройдена — время не измеряем.\nПричина: {e}")
        return 1

    # --- анализ на самом большом размере ---
    summary = analyze_field(res["U"], res["mask"], res["dx"], res["dy"])
    print("\nСводка:", summary)

    # --- сохранение ---
    save_all("results", variant, res["X"], res["Y"], res["U"],
             res["mask"], summary, rows, reports)
    print("\nГотово: ./out/{field_data.npz, summary.json, benchmark.csv, field.png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())