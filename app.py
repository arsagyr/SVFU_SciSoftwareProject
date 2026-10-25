from pathlib import Path
import io
import numpy as np
from flask import Flask, render_template, request, send_file, url_for

from src import calculations, visualization

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def save_metrics(metrics: dict, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")


@app.route("/", methods=["GET", "POST"])
def index():
    context = {"formula": "sin(x*2)", "a": 0.0, "b": 10.0, "n": 900}
    error = None
    metrics = None
    plot_url = None

    if request.method == "POST":
        try:
            # 1. Читаем параметры из формы
            formula = request.form.get("formula", "sin(x)").strip()
            a = float(request.form.get("a", 0))
            b = float(request.form.get("b", 10))
            n = int(request.form.get("n", 900))

            if n < 2:
                raise ValueError("Число точек должно быть ≥ 2")
            if a >= b:
                raise ValueError("Левая граница должна быть меньше правой")

            # 2. Считаем
            calculations.domain.set_formula(formula)
            x, y = calculations.make_data(a, b, n)
            metrics = calculations.calculate_metrics(x, y)

            # 3. Сохраняем файлы результатов
            visualization.save_plot(x, y, RESULTS_DIR / "plot.png", f"y = {formula}")
            np.savetxt(RESULTS_DIR / "data.csv",
                       np.column_stack([x, y]),
                       delimiter=",", header="x,y", comments="", fmt="%.6f")
            save_metrics(metrics, RESULTS_DIR / "metrics.txt")

            # 4. Ссылка на график (с параметром-меткой, чтобы браузер не кэшировал старую картинку)
            plot_url = url_for("get_plot", v=n)

            context.update(formula=formula, a=a, b=b, n=n)

        except Exception as e:
            error = str(e)

    metrics_display = None
    if metrics:
        metrics_display = [
            (calculations.METRIC_LABELS.get(k, k), v) for k, v in metrics.items()
        ]

    return render_template("index.html",
                           **context,
                           metrics=metrics,
                           metrics_display=metrics_display,
                           plot_url=plot_url,
                           error=error)


@app.route("/plot.png")
def get_plot():
    """Отдаёт актуальный график из results/."""
    path = RESULTS_DIR / "plot.png"
    if not path.exists():
        return "График ещё не построен", 404
    return send_file(path, mimetype="image/png")


@app.route("/download/data.csv")
def download_data():
    return send_file(RESULTS_DIR / "data.csv", as_attachment=True,
                     download_name="data.csv")


@app.route("/download/metrics.txt")
def download_metrics():
    return send_file(RESULTS_DIR / "metrics.txt", as_attachment=True,
                     download_name="metrics.txt")


if __name__ == "__main__":
    app.run(debug=True)