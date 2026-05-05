import pandas as pd

def load_household_data(path):
    df = pd.read_csv(path, sep=';', low_memory=False)

    # Combine Date + Time
    df['datetime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'],
        format='%d/%m/%Y %H:%M:%S'
    )

    # Convert power to numeric
    df['Global_active_power'] = pd.to_numeric(
        df['Global_active_power'], errors='coerce'
    )

    # Keep only needed columns
    df = df[['datetime', 'Global_active_power']]

    # Drop missing values
    df = df.dropna()

    return df