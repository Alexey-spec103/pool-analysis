import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_transaction_data
from analyzer import (
    filter_first_n_seconds,
    calculate_price_growth,
    get_average_growth_by_time
)

def main():
    print("Загрузка данных...")

    file_path = 'data/sample_data.csv'
    df = load_transaction_data(file_path)

    print("Первые строки данных:")
    print(df.head())

    print("\nОтбираем первые 10 секунд для каждого пула...")
    filtered_df = filter_first_n_seconds(df, seconds=10)
    print("Результат фильтрации (первые строки):")
    print(filtered_df.head())
    print(f"✅ Всего строк после фильтрации: {len(filtered_df)}")

    print("\nРассчитываем прирост цены во времени...")
    growth_df = calculate_price_growth(filtered_df)
    print("Пример изменения цены по времени:")
    print(growth_df[['timestamp', 'pool_id', 'ms_since_start', 'asset_price_in_usd', 'price_change_pct']].head())

    print("\n📊 Вычисляем среднюю прибыль по времени...")
    time_analysis_df = get_average_growth_by_time(growth_df, time_unit='ms')
    print("Топ 5 моментов по средней прибыли:")
    print(time_analysis_df.sort_values(by='avg_growth_pct', ascending=False).head())

    print("📈 Рисуем и сохраняем график роста прибыли по миллисекундам...")
    plt.figure(figsize=(12, 6))
    plt.plot(time_analysis_df['time'], time_analysis_df['avg_growth_pct'], label='Средняя прибыль (%)')
    plt.title('Средняя прибыль по времени (ms) с момента запуска пула')
    plt.xlabel('Время с начала пула (ms)')
    plt.ylabel('Средняя прибыль (%)')
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 500)
    output_path = 'output/avg_profit_vs_time.png'
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"✅ График сохранён: {output_path}")
    plt.show()

    print("\n💾 Сохраняем отчёт в Excel (avg_profit_report)...")
    time_analysis_df['time_sec'] = time_analysis_df['time'] / 1000
    time_analysis_df['time_sec'] = time_analysis_df['time_sec'].astype(float)
    columns_to_save = ['time_sec', 'avg_growth_pct', 'median_growth_pct', 'max_growth_pct', 'num_trades']
    excel_path = 'output/avg_profit_report.xlsx'
    time_analysis_df[columns_to_save].to_excel(excel_path, index=False)
    print(f"✅ Отчёт сохранён: {excel_path}")

    print("\n📄 Сохраняем сглаженный анализ в Excel (summary_zones.xlsx)...")
    time_analysis_df['avg_growth_smoothed'] = time_analysis_df['avg_growth_pct'].rolling(window=10, min_periods=1).mean()

    def classify_zone(growth):
        if growth > 300 or growth < 10:
            return 'RISK'
        elif 30 <= growth <= 200:
            return 'BUY'
        else:
            return 'NEUTRAL'

    time_analysis_df['zone'] = time_analysis_df['avg_growth_smoothed'].apply(classify_zone)

    summary = time_analysis_df[['time_sec', 'avg_growth_pct', 'avg_growth_smoothed', 'zone', 'num_trades']]
    summary = summary.round({'time_sec': 3, 'avg_growth_pct': 2, 'avg_growth_smoothed': 2})
    summary_path = 'output/summary_zones.xlsx'
    summary.to_excel(summary_path, index=False)
    print(f"✅ Сглаженная таблица сохранена: {summary_path}")

    print("\n📥 Создаём симуляцию по миллисекундам...")
    bribe_fee = 0.0
    investment = 1.0
    results = []

    for ms in range(0, 10000):
        time_s = ms / 1000
        frame = summary[summary['time_sec'] >= time_s]

        if frame.empty:
            continue

        avg_profit = frame['avg_growth_smoothed'].mean()
        return_sol = investment * (1 + (avg_profit - bribe_fee) / 100)
        total_trades = frame['num_trades'].sum()

        results.append({
            'time_ms': ms,
            'time_sec': round(time_s, 3),
            'avg_profit_pct': round(avg_profit, 3),
            'return_SOL': round(return_sol, 4),
            'total_trades': int(total_trades)
        })

    sim_ms_df = pd.DataFrame(results)
    sim_ms_path = 'output/simulation_per_ms.xlsx'
    sim_ms_df.to_excel(sim_ms_path, index=False)
    print(f"✅ Симуляция по миллисекундам сохранена: {sim_ms_path}")

    print("\n📥 Сохраняем интервал анализа (1 секунда)...")
    interval_df = summary.copy()
    interval_df['time_bucket'] = interval_df['time_sec'].apply(lambda x: f"{int(x)}–{int(x)+1}")
    grouped_1s = interval_df.groupby('time_bucket').agg(
        avg_profit=('avg_growth_smoothed', 'mean'),
        max_profit=('avg_growth_smoothed', 'max'),
        min_profit=('avg_growth_smoothed', 'min'),
        num_trades=('num_trades', 'sum')
    ).reset_index()

    def risk_label(row):
        if row['max_profit'] > 300 or row['min_profit'] < 0:
            return 'HIGH'
        elif 30 <= row['avg_profit'] <= 200:
            return 'LOW'
        else:
            return 'MEDIUM'

    grouped_1s['risk'] = grouped_1s.apply(risk_label, axis=1)
    grouped_1s = grouped_1s.round(2)
    grouped_1s.to_excel('output/interval_summary.xlsx', index=False)
    print("✅ Таблица интервалов (1s) сохранена: output/interval_summary.xlsx")

    print("\n📥 Создаём интервал анализа по 0.5 секунды...")
    interval_df['interval_0_5s'] = interval_df['time_sec'].apply(
        lambda x: f"{round(x - (x % 0.5), 1):.1f}–{round(x - (x % 0.5) + 0.5, 1):.1f}"
    )

    grouped_05s = interval_df.groupby('interval_0_5s').agg(
        avg_profit=('avg_growth_smoothed', 'mean'),
        max_profit=('avg_growth_smoothed', 'max'),
        min_profit=('avg_growth_smoothed', 'min'),
        total_trades=('num_trades', 'sum')
    ).reset_index()

    grouped_05s['risk'] = grouped_05s.apply(risk_label, axis=1)
    grouped_05s = grouped_05s.round(2)
    grouped_05s.to_excel('output/interval_summary_05s.xlsx', index=False)
    print("✅ Таблица интервалов (0.5s) сохранена: output/interval_summary_05s.xlsx")

    print("\n✅ Всё готово! Переходим к Dashboard или симуляции.")

if __name__ == '__main__':
    main()
