import numpy as np
from src.data_loader import load_household_data
from src.features import create_features
from src.lstm_model import load_lstm
from src.xgb_model import load_xgb
from src.isolation_forest_model import load_isolation_forest, predict_anomaly_if
from src.hybrid_model import hybrid_predict
from src.anomaly import detect_anomaly

WINDOW = 10

print("\nLoading system...")

# Load models
model, scaler = load_lstm()
xgb_model = load_xgb()
if_model = load_isolation_forest()

print("Models loaded successfully")

# Load data
df = load_household_data("data/household.txt")
df = create_features(df)

# Latest window
latest_window = df['Global_active_power'].values[-WINDOW:]

# Feature row for models
features_row = df.iloc[-1][[
    'hour',
    'day_of_week',
    'lag_1',
    'lag_2',
    'lag_3',
    'rolling_mean_5',
    'rolling_std_5'
]].values

# Hybrid prediction
final_pred = hybrid_predict(
    model,
    scaler,
    xgb_model,
    latest_window,
    features_row
)

actual = df['Global_active_power'].iloc[-1]

# Deviation anomaly
rolling_std = df['rolling_std_5'].iloc[-1]

dev_status, deviation, threshold = detect_anomaly(
    actual,
    final_pred,
    rolling_std
)

# Isolation Forest anomaly
if_features = df.iloc[-1][[
    'Global_active_power',
    'hour',
    'day_of_week',
    'lag_1',
    'lag_2',
    'lag_3',
    'rolling_mean_5',
    'rolling_std_5'
]].values

if_status = predict_anomaly_if(if_model, if_features)

# Final decision
final_status = "ANOMALY" if (
    dev_status == "ANOMALY" or if_status == "ANOMALY"
) else "NORMAL"

# Output
print("\n========== EMS OUTPUT ==========")
print(f"Predicted : {final_pred:.4f}")
print(f"Actual    : {actual:.4f}")
print(f"Deviation : {deviation:.4f} (threshold {threshold:.4f})")
print(f"Dev Status: {dev_status}")
print(f"IF Status : {if_status}")
print(f"FINAL     : {final_status}")
print("================================\n")