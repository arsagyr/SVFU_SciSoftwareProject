# Импортируйте matplotlib.pyplot и создайте функцию save_plot(x, y, path, title).
# - создать рисунок размером 8 × 4 дюйма
# - построить линию по массивам x и y
# - подписать обе оси, добавить сетку и заголовок
# - сохранить рисунок по переданному пути в формате PNG с dpi=150
# - закрыть рисунок после сохранения

# Разделение обязанностей: функция получает готовые данные и
# путь. Она не вычисляет формулу и не выбирает каталог результатов.

import matplotlib.pyplot as plt


def save_plot(x, y, path, title):
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(x, y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.grid(True)

    fig.savefig(path, format="png", dpi=150)
    plt.close(fig)