from sklearn.ensemble import IsolationForest
import joblib


def train_isolation_forest(df):
    features = [
        'Global_active_power',
        'hour',
        'day_of_week',
        'lag_1',
        'lag_2',
        'lag_3',
        'rolling_mean_5',
        'rolling_std_5'
    ]

    X = df[features]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.01,
        random_state=42
    )

    model.fit(X)

    # Save model
    joblib.dump(model, "models/isolation_forest.pkl")

    return model


# predict anomalies
def predict_anomaly_if(model, feature_row):
    result = model.predict([feature_row])[0]

    if result == -1:
        return "ANOMALY"
    return "NORMAL"


def load_isolation_forest():
    import joblib
    return joblib.load("models/isolation_forest.pkl")