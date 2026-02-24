import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_listening_events(
    n_users=500,
    days=14,
    anomaly_ratio=0.05,
    seed=42
):
    np.random.seed(seed)

    events = []
    start_date = datetime.now() - timedelta(days=days)

    anomalous_users = set(
        np.random.choice(
            range(n_users),
            size=int(n_users * anomaly_ratio),
            replace=False
        )
    )

    for user_id in range(n_users):
        base_daily_minutes = max(10, np.random.normal(60, 20))

        for day in range(days):
            date = start_date + timedelta(days=day)

            sessions = max(1, np.random.poisson(3))

            for _ in range(sessions):
                hour = np.random.choice(
                    range(24),
                    p=hour_distribution(user_id in anomalous_users)
                )

                timestamp = date.replace(hour=hour, minute=0)

                duration = np.random.normal(
                    base_daily_minutes / sessions * 60,
                    300
                )

                if user_id in anomalous_users and np.random.rand() < 0.3:
                    duration *= np.random.uniform(3, 6)

                events.append({
                    "user_id": user_id,
                    "timestamp": timestamp,
                    "track_id": np.random.randint(1, 10000),
                    "listening_duration_sec": max(30, duration)
                })

    return pd.DataFrame(events)


def hour_distribution(is_anomalous):
    if not is_anomalous:
        probs = np.ones(24)
        probs[8:23] = 3  # gündüz/akşam daha aktif
    else:
        probs = np.ones(24)
        probs[0:5] = 4   # gece anomali

    return probs / probs.sum()


if __name__ == "__main__":
    df = generate_listening_events()
    df.to_csv("data/raw/listening_events.csv", index=False)