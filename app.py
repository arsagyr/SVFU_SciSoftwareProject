from pathlib import Path
import numpy as np
from flask import Flask, render_template, request, send_file, url_for

from src import classes, visualization, calculations



domain = classes.Whole_Domain(formula = 'x')

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
    context = {"formula": "sin(x**2)", "a": 0.0, "b": "sqrt(8 * pi)", "n": 900}
    error = None
    metrics = None
    plot_url = None

    if request.method == "POST":
        try:
            # 1. Читаем параметры из формы
            formula = request.form.get("formula", "sin(x)").strip()
            domain.min_x = calculations.parse_value(request.form["a"])
            domain.max_x = calculations.parse_value(request.form["b"])
            domain.formula = formula
            n = int(request.form.get("n", 900))
            

            # 2. Считаем
            x,y = domain.make_data(n)
            metrics = domain.calculate_metrics(x,y)

            # 3. Сохраняем файлы результатов
            visualization.save_plot(x, y, RESULTS_DIR / "plot.png", f"y = {formula}")
            np.savetxt(RESULTS_DIR / "data.csv",
                       np.column_stack([x, y]),
                       delimiter=",", header="x,y", comments="", fmt="%.6f")
            save_metrics(metrics, RESULTS_DIR / "metrics.txt")

            # 4. Ссылка на график (с параметром-меткой, чтобы браузер не кэшировал старую картинку)
            plot_url = url_for("get_plot", v=n)

            context.update(formula=formula, a=domain.min_x, b=domain.max_x, n=n)

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