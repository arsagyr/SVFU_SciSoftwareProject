# 2D field: loop vs NumPy

Расчёт u(x,y) = sin(2x+y) + cos(x−2y) на сетке центров ячеек.
Две реализации (Python-циклы и broadcasting) валидируются перед
замерами и сравниваются по времени.

## Запуск
pip install -r requirements.txt
python main.py

## Артефакты (./out)
- field_data.npz   — X, Y, U, mask
- summary.json     — вариант, статистика, отчёт валидации
- benchmark.csv    — ny, nx, t_loop, t_numpy, speedup
- field.png        — карта поля с контуром маски