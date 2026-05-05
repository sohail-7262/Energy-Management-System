import os

from data_loader import load_household_data
from features import create_features
from lstm_model import train_lstm, load_lstm
from xgb_model import train_xgb
from hybrid_model import hybrid_predict
from anomaly import detect_anomaly
from isolation_forest_model import (
    train_isolation_forest,
    predict_anomaly_if
)

# =========================
# CONFIG
# =========================
DATA_PATH = "data/household.txt"
WINDOW_SIZE = 10


# =========================
# STEP 1: LOAD DATA
# =========================
print("\nLoading dataset...")
df = load_household_data(DATA_PATH)

print("Creating features...")
df = create_features(df)

# LSTM 
window = 10
if os.path.exists("models/lstm.h5"):
    print("Loading LSTM model...")
    model, scaler = load_lstm()
# still need predictions for XGBoost training
    # _, _, preds, actual = train_lstm(df['Global_active_power'], window)
else:
    pass 
    # print("Training LSTM model...") 
    # model, scaler, preds, actual = train_lstm( df['Global_active_power'], window )
