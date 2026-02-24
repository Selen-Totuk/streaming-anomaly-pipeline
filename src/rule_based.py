import pandas as pd


def detect_anomalies_rule_based(
    df: pd.DataFrame,
    k: float = 3.0
) -> pd.DataFrame:
    """
    Detect anomalies using user-specific mean and standard deviation.
    """

    df = df.copy()
    df["is_anomaly"] = False

    for user_id, group in df.groupby("user_id"):
        stats = group[[
            "total_listening_sec",
            "track_count",
            "avg_session_sec",
            "night_ratio"
        ]].agg(["mean", "std"])

        for idx, row in group.iterrows():
            score = 0

            for feature in stats.columns:
                mean = stats.loc["mean", feature]
                std = stats.loc["std", feature]

                if std == 0:
                    continue

                z = abs(row[feature] - mean) / std

                if z > k:
                    score += 1

            # Basit ama bilinçli kural:
            # Birden fazla sinyal aynı anda sapıyorsa
            if score >= 2:
                df.loc[idx, "is_anomaly"] = True

    return df


if __name__ == "__main__":
    features = pd.read_csv("data/processed/daily_user_features.csv")
    results = detect_anomalies_rule_based(features)

    results.to_csv(
        "data/processed/rule_based_results.csv",
        index=False
    )