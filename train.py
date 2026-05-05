import numpy as np
from src.data_loader import load_household_data
from src.features import create_features
from src.lstm_model import train_lstm
from src.xgb_model import train_xgb
from src.isolation_forest_model import train_isolation_forest

WINDOW = 10

print("Loading data...")
df = load_household_data("data/household.txt")

print("Creating features...")
df = create_features(df)

print("Training LSTM...")
model, scaler, preds, actual = train_lstm(
    df['Global_active_power'], WINDOW
)

# Save predictions
np.save("models/lstm_preds.npy", preds)
np.save("models/lstm_actual.npy", actual)

# Align
df_model = df.iloc[WINDOW:].copy()
df_model['predicted'] = preds
df_model['actual'] = actual

print("Training XGBoost...")
train_xgb(df_model)

print("Training Isolation Forest...")
train_isolation_forest(df_model)

print("\n✅ TRAINING COMPLETE — MODELS SAVED")