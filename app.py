import streamlit as st
import numpy as np
from pathlib import Path
import io
import sys

# Предполагаем, что ваши модули находятся в src/
sys.path.append(str(Path(__file__).resolve().parent))
from src import calculations, visualization

st.set_page_config(page_title="Анализ функции", layout="wide")
st.title("📈 Интерактивный анализ функции")

# --- Боковая панель для ввода параметров ---
with st.sidebar:
    st.header("Параметры")
    formula_str = st.text_area("Формула (используйте x)", value="sin(x*2)", height=100)
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Начало интервала (a)", value=0.0, step=0.1)
    with col2:
        b = st.number_input("Конец интервала (b)", value=10.0, step=0.1)
    n = st.slider("Число точек", min_value=10, max_value=5000, value=900, step=10)
    
    run_button = st.button("🚀 Выполнить расчёт", type="primary")

# --- Основная область ---
if run_button:
    try:
        # 1. Установка формулы
        calculations.domain.set_formula(formula_str)
        
        # 2. Генерация данных
        x, y = calculations.make_data(a, b, n)
        
        # 3. Вычисление метрик
        metrics = calculations.calculate_metrics(x, y)
        
        # 4. Отображение графика
        # Вариант А: если save_plot умеет возвращать fig
        # fig = visualization.save_plot(x, y, path=None, title=f"y = {formula_str}", return_fig=True)
        # st.pyplot(fig)
        
        # Вариант Б: создаём график прямо здесь для Streamlit
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x, y)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"y = {formula_str}")
        ax.grid(True)
        st.pyplot(fig)
        plt.close(fig)
        
        # 5. Отображение метрик
        st.subheader("Результаты расчёта")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Среднее", f"{metrics['mean']:.4f}")
        col_m2.metric("Минимум", f"{metrics['min']:.4f}")
        col_m3.metric("Максимум", f"{metrics['max']:.4f}")
        
        with st.expander("Показать все метрики"):
            st.json(metrics)
        
        # 6. Таблица с данными
        st.subheader("Данные")
        # Преобразуем в формат, понятный st.dataframe
        data_for_df = {"x": x, "y": y}
        st.dataframe(data_for_df, use_container_width=True)
        
        # 7. Кнопки для скачивания
        # CSV с данными
        csv_buffer = io.StringIO()
        np.savetxt(csv_buffer, np.column_stack([x, y]), delimiter=",", header="x,y", comments="", fmt="%.6f")
        st.download_button(
            label="📥 Скачать data.csv",
            data=csv_buffer.getvalue(),
            file_name="data.csv",
            mime="text/csv",
        )
        
        # TXT с метриками
        metrics_text = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
        st.download_button(
            label="📥 Скачать metrics.txt",
            data=metrics_text,
            file_name="metrics.txt",
            mime="text/plain",
        )
        
    except Exception as e:
        st.error(f"Ошибка при расчёте: {e}")