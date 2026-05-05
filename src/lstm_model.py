import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
import joblib





# ---- CREATE SEQUENCES ----
def create_sequences(data, window=10):
    X, y = [], []

    for i in range(window, len(data)):
        X.append(data[i-window:i])
        y.append(data[i])

    return np.array(X), np.array(y)


# ---- PREPARE DATA ----
def prepare_lstm(series, window=10):
    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(series.values.reshape(-1, 1))

    X, y = create_sequences(scaled, window)

    return X, y, scaler


# ---- TRAIN MODEL ----
def train_lstm(series, window=10):
    X, y, scaler = prepare_lstm(series, window)

    model = Sequential([
        LSTM(64, input_shape=(window, 1)),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    print("Training LSTM...")
    model.fit(X, y, epochs=5, batch_size=32)

    # ---- PREDICTIONS ----
    preds = model.predict(X)

    # Convert back to original scale
    preds = scaler.inverse_transform(preds)
    actual = scaler.inverse_transform(y)

    # Save model (future AWS use)
    model.save("models/lstm.h5")
    joblib.dump(scaler, "models/lstm_scaler.pkl")

    return model, scaler, preds.flatten(), actual.flatten()


# ---- LOAD SAVED MODEL ----
def load_lstm():
    model = load_model("models/lstm.h5", compile=False)
    scaler = joblib.load("models/lstm_scaler.pkl")
    return model, scaler