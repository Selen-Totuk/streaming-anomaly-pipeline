import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_comparison():
    df = pd.read_csv("data/processed/comparison_results.csv")
    
    plt.figure(figsize=(12, 7))
    
    # Karar gruplarını renklendirelim
    colors = {
        "both": "#e74c3c",      # Kırmızı (Kesin anomali)
        "ml_only": "#3498db",   # Mavi (Gizli pattern)
        "rule_only": "#f1c40f", # Sarı (Uç değer)
        "none": "#bdc3c7"       # Gri (Normal)
    }

    sns.scatterplot(
        data=df,
        x="total_listening_sec",
        y="night_ratio",
        hue="decision_group",
        palette=colors,
        alpha=0.6,
        edgecolor="w"
    )

    plt.title("When Patterns Break: Rule-Based vs ML Detection", fontsize=14)
    plt.axvline(x=64800, color='gray', linestyle='--', alpha=0.5, label='18h Threshold')
    plt.legend(title="Detection Group")
    plt.tight_layout()
    plt.savefig("data/processed/anomaly_landscape.png")
   
    print("Gorsellestirme kaydedildi: data/processed/anomaly_landscape.png")

if __name__ == "__main__":
    plot_comparison()