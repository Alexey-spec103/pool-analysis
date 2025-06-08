import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(layout='wide')
st.title("📊 Анализ запуска пула и оптимального момента покупки")

# --- График: Средняя прибыль по миллисекундам ---
st.header("📉 Средняя прибыль по миллисекундам")
st.image(os.path.join("output", "avg_profit_vs_time.png"), use_column_width=True)

# --- График: Средняя прибыль по 1 сек ---
st.header("📈 Средняя прибыль по 1-секундным интервалам")
st.image(os.path.join("output", "graph_interval_1s.png"), use_column_width=True)

# --- График: Средняя прибыль по 0.5 сек ---
st.header("📈 Средняя прибыль по 0.5-секундным интервалам")
st.image(os.path.join("output", "graph_interval_05s.png"), use_column_width=True)

# --- График: Риск ---
st.header("🔥 Уровень риска по интервалам")
st.image(os.path.join("output", "graph_risk_levels.png"), use_column_width=True)

# --- График: Симуляция ---
st.header("🧠 Симуляция доходности по миллисекундам")
st.image(os.path.join("output", "graph_simulation_returns.png"), use_column_width=True)

# --- Просмотр таблиц ---
st.header("📋 Финальные таблицы")
tab1, tab2, tab3 = st.tabs(["Зоны", "Интервалы", "Симуляция"])

with tab1:
    st.subheader("Сглаженные зоны")
    df1 = pd.read_excel(os.path.join("output", "summary_zones.xlsx"))
    st.dataframe(df1)

with tab2:
    st.subheader("Интервалы (1 секунда)")
    df2 = pd.read_excel(os.path.join("output", "interval_summary.xlsx"))
    st.dataframe(df2)

    st.subheader("Интервалы (0.5 секунды)")
    df3 = pd.read_excel(os.path.join("output", "interval_summary_05s.xlsx"))
    st.dataframe(df3)

with tab3:
    st.subheader("Симуляция по миллисекундам")
    df4 = pd.read_excel(os.path.join("output", "simulation_per_ms.xlsx"))
    st.dataframe(df4)
