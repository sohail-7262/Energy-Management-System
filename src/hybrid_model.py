def hybrid_predict(lstm_model, scaler, xgb_model, window_data, feature_row):
    import numpy as np

    # LSTM prediction
    scaled = scaler.transform(window_data.reshape(-1, 1))
    X = np.array([scaled])

    lstm_pred = lstm_model.predict(X)[0][0]
    lstm_pred = scaler.inverse_transform([[lstm_pred]])[0][0]

    # Add LSTM prediction to features
    feature_row = list(feature_row) + [lstm_pred]

    # XGBoost correction
    residual = xgb_model.predict([feature_row])[0]

    final_pred = lstm_pred + residual

    return final_pred