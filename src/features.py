import pandas as pd
import numpy as np

def create_features(df):
    df = df.copy()

    df = df.set_index('datetime')

    # -------------------------
    # TIME FEATURES
    # -------------------------
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek

    # -------------------------
    # LAG FEATURES
    # -------------------------
    df['lag_1'] = df['Global_active_power'].shift(1)
    df['lag_2'] = df['Global_active_power'].shift(2)
    df['lag_3'] = df['Global_active_power'].shift(3)

    # -------------------------
    # ROLLING FEATURES
    # -------------------------
    df['rolling_mean_5'] = df['Global_active_power'].rolling(5).mean()
    df['rolling_std_5'] = df['Global_active_power'].rolling(5).std()

    # -------------------------
    # ⚡ SIMULATED APPLIANCE FEATURES
    # -------------------------
    # (until we integrate UK-DALE)

    df['fridge_usage'] = np.random.uniform(0.1, 0.3, len(df))
    df['ac_usage'] = np.where(df['hour'].between(12, 18),
                             np.random.uniform(1.0, 2.5, len(df)),
                             np.random.uniform(0.0, 0.5, len(df)))

    df['washing_machine'] = np.where(df['hour'].isin([8, 20]),
                                    np.random.uniform(0.5, 1.5, len(df)),
                                    0)

    # -------------------------
    # 🌦️ SIMULATED WEATHER FEATURES
    # -------------------------
    df['temperature'] = 20 + 10 * np.sin(2 * np.pi * df['hour'] / 24)
    df['humidity'] = 50 + 20 * np.cos(2 * np.pi * df['hour'] / 24)

    # -------------------------
    # FINAL CLEANUP
    # -------------------------
    df = df.dropna()

    return df