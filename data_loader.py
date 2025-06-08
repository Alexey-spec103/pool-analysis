# data_loader.py

import pandas as pd

def load_transaction_data(file_path):
    try:
        # Загружаем CSV
        df = pd.read_csv(file_path)

        # Преобразуем колонку времени в datetime с миллисекундами
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Сортируем по времени от старых к новым
        df = df.sort_values(by='timestamp').reset_index(drop=True)

        return df

    except Exception as e:
        print("Ошибка при загрузке файла:", e)
        return None
