# analyzer.py

import pandas as pd

def filter_first_n_seconds(df, seconds=10):
    """
    Возвращает DataFrame, содержащий только транзакции, которые произошли в первые N секунд
    после первой транзакции в каждом пуле.
    """
    result = []

    # Группируем по pool_id
    grouped = df.groupby('pool_id')

    for pool_id, group in grouped:
        group = group.sort_values(by='timestamp')
        first_time = group['timestamp'].iloc[0]
        time_limit = first_time + pd.Timedelta(seconds=seconds)

        filtered = group[group['timestamp'] <= time_limit]
        result.append(filtered)

    return pd.concat(result).reset_index(drop=True)

def calculate_price_growth(df):
    """
    Для каждой строки считает, сколько миллисекунд прошло с момента появления пула,
    и на сколько процентов изменилась цена от начальной.
    """
    df = df.copy()
    result = []

    grouped = df.groupby('pool_id')

    for pool_id, group in grouped:
        group = group.sort_values(by='timestamp')
        start_time = group['timestamp'].iloc[0]
        start_price = group['asset_price_in_usd'].iloc[0]

        group['ms_since_start'] = (group['timestamp'] - start_time).dt.total_seconds() * 1000
        group['ms_since_start'] = group['ms_since_start'].astype(int)

        group['price_change_pct'] = ((group['asset_price_in_usd'] - start_price) / start_price) * 100

        result.append(group)

    return pd.concat(result).reset_index(drop=True)


def get_average_growth_by_time(df, time_unit='ms'):
    """
    Возвращает таблицу со средней прибылью в зависимости от прошедшего времени.
    time_unit: 'ms' = миллисекунды, 's' = секунды
    """
    df = df.copy()

    if time_unit == 's':
        df['time_bucket'] = df['ms_since_start'] // 1000
    else:
        df['time_bucket'] = df['ms_since_start']

    grouped = df.groupby('time_bucket')['price_change_pct'].agg(['mean', 'median', 'max', 'count']).reset_index()
    grouped = grouped.rename(columns={
        'time_bucket': 'time',
        'mean': 'avg_growth_pct',
        'median': 'median_growth_pct',
        'max': 'max_growth_pct',
        'count': 'num_trades'
    })

    return grouped
