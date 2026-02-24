import pandas as pd


def extract_daily_user_features(events: pd.DataFrame) -> pd.DataFrame:
    df = events.copy()
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour

    daily = (
        df.groupby(["user_id", "date"])
        .agg(
            total_listening_sec=("listening_duration_sec", "sum"),
            track_count=("track_id", "nunique"),
            avg_session_sec=("listening_duration_sec", "mean"),
            night_ratio=("hour", lambda x: (x < 6).mean())
        )
        .reset_index()
    )

    return daily


if __name__ == "__main__":
    events = pd.read_csv("data/raw/listening_events.csv")
    daily_features = extract_daily_user_features(events)
    daily_features.to_csv(
        "data/processed/daily_user_features.csv",
        index=False
    )