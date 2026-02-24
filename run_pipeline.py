import subprocess
import sys


STEPS = [
    "src/data_generation.py",
    "src/feature_engineering.py",
    "src/rule_based.py",
    "src/ml_based.py",
    "src/evaluation.py",
    "src/visualize_results.py"  # <-- Yeni adım
]


def run_step(script_path):
    print(f"\n▶ Running {script_path}")
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"✖ Error in {script_path}")
        print(result.stderr)
        sys.exit(1)

    print(f"✔ Completed {script_path}")


if __name__ == "__main__":
    print("Starting anomaly detection pipeline...\n")

    for step in STEPS:
        run_step(step)

    print("\nPipeline finished successfully.")