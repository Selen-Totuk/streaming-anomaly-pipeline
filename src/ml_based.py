import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "total_listening_sec",
    "track_count",
    "avg_session_sec",
    "night_ratio"
]


def detect_anomalies_ml(
    df: pd.DataFrame,
    contamination: float = 0.05,
    random_state: int = 42
) -> pd.DataFrame:
    df = df.copy()

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=random_state
    )

    X = df[FEATURE_COLUMNS]
    preds = model.fit_predict(X)

    # sklearn: -1 = anomaly, 1 = normal
    df["is_anomaly_ml"] = preds == -1
    df["anomaly_score"] = model.decision_function(X)

    return df


if __name__ == "__main__":
    features = pd.read_csv("data/processed/daily_user_features.csv")

    results = detect_anomalies_ml(features)

    results.to_csv(
        "data/processed/ml_based_results.csv",
        index=False
    )