import csv
import json
import os


def _ensure_dir(path: str):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)


def save_results_to_json(data, path: str):
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def save_results_to_csv(integration_results: dict, path: str):
    _ensure_dir(path)
    if not integration_results:
        return

    rows = []
    for key, vals in integration_results.items():
        n = int(key.split("_")[1])
        rows.append((n, vals))
    rows.sort(key=lambda t: t[0])

    fieldnames = ["n", "T_n", "method_difference", "actual_error_Tn"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for n, vals in rows:
            w.writerow({
                "n": n,
                "T_n": vals.get("T_n"),
                "method_difference": vals.get("method_difference"),
                "actual_error_Tn": vals.get("actual_error_Tn"),
            })