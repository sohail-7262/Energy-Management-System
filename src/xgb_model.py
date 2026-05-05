from xgboost import XGBRegressor
import joblib


def train_xgb(df):
    df = df.copy()

    # Residual = error of LSTM
    df['residual'] = df['actual'] - df['predicted']

    features = [
        'hour',
        'day_of_week',
        'lag_1',
        'lag_2',
        'lag_3',
        'rolling_mean_5',
        'rolling_std_5',
        'predicted'   # LSTM prediction
    ]

    X = df[features]
    y = df['residual']

    model = XGBRegressor(n_estimators=200, max_depth=5)
    model.fit(X, y)

    # Save model (future AWS use)
    joblib.dump(model, "models/xgb.pkl")

    return model

def load_xgb():
    return joblib.load("models/xgb.pkl")