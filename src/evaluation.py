import pandas as pd


def compare_methods(rule_df: pd.DataFrame, ml_df: pd.DataFrame) -> pd.DataFrame:
    df = rule_df.merge(
        ml_df[["user_id", "date", "is_anomaly_ml", "anomaly_score"]],
        on=["user_id", "date"],
        how="inner"
    )

    def label(row):
        if row["is_anomaly"] and row["is_anomaly_ml"]:
            return "both"
        if row["is_anomaly"] and not row["is_anomaly_ml"]:
            return "rule_only"
        if not row["is_anomaly"] and row["is_anomaly_ml"]:
            return "ml_only"
        return "none"

    df["decision_group"] = df.apply(label, axis=1)
    return df


if __name__ == "__main__":
    rule_results = pd.read_csv("data/processed/rule_based_results.csv")
    ml_results = pd.read_csv("data/processed/ml_based_results.csv")

    comparison = compare_methods(rule_results, ml_results)

    comparison.to_csv(
        "data/processed/comparison_results.csv",
        index=False
    )