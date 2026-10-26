# В основном файле:
# - импортируйте Path, NumPy и функции из двух созданных модулей
# - определите корень проекта через Path(__file__).resolve().parent
# - сформируйте путь к каталогу results/
# - создайте функцию main()
# - внутри main() задайте номер варианта, границы интервала и число точек
# - создайте каталог результатов
# - вызовите make_data и calculate_metrics

# Ограничение: формула варианта и вычисление характеристик
# должны находиться в calculations.py.

# После вычислений программа должна:
# - записать x и y в data.csv с заголовком x,y
# - записать семь подписанных значений в metrics.txt
# - передать данные, путь и заголовок в save_plot
# - сохранить график под именем plot.png
# - вывести в терминал путь к каталогу результатов
# - вызвать main() только при непосредственном запуске файла
# Проверка структуры: в main.py остаются параметры и порядок
# действий, а не формулы и оформление графика.

from pathlib import Path
from math import pi, sqrt
import numpy as np
from src import calculations, visualization

def save_metrics(metrics: dict, path: Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")

def save_xy_csv(x, y, path: Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.column_stack([x, y])                 
    np.savetxt(path, data, delimiter=",",
               header="x,y", comments="", fmt="%.6f")
               
def main():
    root = Path(__file__).resolve().parent
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    calculations.domain.set_formula('sin(x*2)')
    x, y = calculations.make_data(0, 10, sqrt(8 * pi))
    metrics = calculations.calculate_metrics(x,y)

    print(x, '\n', y)
    print(metrics)

    save_xy_csv(x,y, results_dir / "xy.csv")
    save_metrics(metrics, results_dir / "metrics.txt")
    visualization.save_plot(x, y, path = results_dir / 'plot.png', title ='Результаты')
    

if __name__ == "__main__":
    main()
 
 
