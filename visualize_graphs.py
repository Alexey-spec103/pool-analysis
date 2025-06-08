import pandas as pd
import matplotlib.pyplot as plt

# Загружаем таблицы
df_sim = pd.read_excel('output/simulation_per_ms.xlsx')
df_1s = pd.read_excel('output/interval_summary.xlsx')
df_05s = pd.read_excel('output/interval_summary_05s.xlsx')

# === 1. Доходность по миллисекундам ===
plt.figure(figsize=(12, 5))
plt.plot(df_sim['time_sec'], df_sim['return_SOL'], label='Доходность (SOL)')
plt.xlabel('Время (секунды)')
plt.ylabel('Доходность (SOL)')
plt.title('Симуляция доходности по миллисекундам')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('output/graph_simulation_returns.png')
plt.close()

# === 2. Средняя прибыль по 1-секундным интервалам ===
plt.figure(figsize=(12, 5))
plt.plot(df_1s['time_bucket'], df_1s['avg_profit'], marker='o', label='Средняя прибыль (%)')
plt.xlabel('Интервал (1 секунда)')
plt.ylabel('Средняя прибыль (%)')
plt.title('Средняя прибыль по 1-секундным интервалам')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('output/graph_interval_1s.png')
plt.close()

# === 3. Средняя прибыль по 0.5-секундным интервалам ===
plt.figure(figsize=(12, 5))
plt.plot(df_05s['interval_0_5s'], df_05s['avg_profit'], marker='o', label='Средняя прибыль (%)')
plt.xlabel('Интервал (0.5 секунды)')
plt.ylabel('Средняя прибыль (%)')
plt.title('Средняя прибыль по 0.5-секундным интервалам')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('output/graph_interval_05s.png')
plt.close()

# === 4. График риска по 1-секундным интервалам ===
color_map = {'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
colors = df_1s['risk'].map(color_map)

plt.figure(figsize=(12, 5))
plt.bar(df_1s['time_bucket'], df_1s['avg_profit'], color=colors)
plt.xlabel('Интервал (1 секунда)')
plt.ylabel('Средняя прибыль (%)')
plt.title('Уровень риска по интервалам')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('output/graph_risk_levels.png')
plt.close()
