import joblib
import numpy as np
from tensorflow.keras.models import load_model


def input_fn(request_body, request_content_type):
    import json
    return json.loads(request_body)


def output_fn(prediction, content_type):
    import json
    return json.dumps(prediction)



# load models
def model_fn(model_dir):
    lstm = load_model(model_dir + "/lstm.h5", compile=False)
    scaler = joblib.load(model_dir + "/lstm_scaler.pkl")
    xgb = joblib.load(model_dir + "/xgb.pkl")
    iso = joblib.load(model_dir + "/isolation_forest.pkl")

    return {
        "lstm": lstm,
        "scaler": scaler,
        "xgb": xgb,
        "iso": iso
    }

# prediction logic
def predict_fn(input_data, model):
    lstm = model["lstm"]
    scaler = model["scaler"]
    xgb = model["xgb"]
    iso = model["iso"]

    data = np.array(input_data)

    # assume last column = energy window
    window = data[:, :10]
    features = data[:, 10:]

    # LSTM prediction
    scaled = scaler.transform(window.reshape(-1, 1))
    X = np.array([scaled])
    lstm_pred = lstm.predict(X)[0][0]
    lstm_pred = scaler.inverse_transform([[lstm_pred]])[0][0]

    # XGB correction
    feature_row = list(features[0]) + [lstm_pred]
    residual = xgb.predict([feature_row])[0]

    final_pred = lstm_pred + residual

    # Isolation Forest
    iso_result = iso.predict([feature_row])[0]

    # ---- NEW: deviation logic ----
    actual = window[-1][-1]   # last value in window
    rolling_std = np.std(window)

    deviation = actual - final_pred
    threshold = 2 * rolling_std

    if deviation > threshold:
        dev_status = "HIGH_USAGE"
    elif deviation < -threshold:
        dev_status = "LOW_USAGE"
    else:
        dev_status = "NORMAL"

    # ---- FINAL DECISION ----
    if dev_status == "HIGH_USAGE" or iso_result == -1:
        final_status = "ALERT"
    elif dev_status == "LOW_USAGE":
        final_status = "OPTIMAL"
    else:
        final_status = "NORMAL"

    return {
        "prediction": float(final_pred),
        "actual": float(actual),
        "deviation": float(deviation),
        "status": final_status
    }