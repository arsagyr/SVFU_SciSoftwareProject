import json
import csv
import os

def save_results_to_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Результаты сохранены в {filepath}")

def save_results_to_csv(data_dict, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Преобразуем словарь словарей в список строк для CSV
    # Ожидаем, что data_dict имеет вид: {"n_50": {"Tn": ..., "diff": ...}, "n_100": {...}}
    rows = []
    for key, metrics in data_dict.items():
        row = {"Parameter": key}
        row.update(metrics)
        rows.append(row)
        
    if not rows:
        return
        
    fieldnames = ["Parameter"] + list(rows[0].keys())[1:]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Результаты сохранены в {filepath}")