def detect_anomaly(actual, predicted, rolling_std, alpha=2):
    deviation = actual - predicted   # IMPORTANT CHANGE

    threshold = alpha * rolling_std

    if deviation > threshold:
        return "HIGH_USAGE", deviation, threshold
    elif deviation < -threshold:
        return "LOW_USAGE", deviation, threshold
    else:
        return "NORMAL", deviation, threshold