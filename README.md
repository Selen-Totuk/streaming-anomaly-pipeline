# When Listening Patterns Break
## Detecting Abnormal User Behavior in Music Streaming

Music streaming platforms rely on user listening patterns to drive recommendations, analytics, and revenue.

But what happens when those patterns break?

This project explores how abnormal listening behavior can be detected using simple statistical reasoning and machine learning — starting from raw event logs.

Rather than labeling users as anomalous, the system evaluates **user-day behavior**, flagging a day as anomalous only when **multiple independent signals deviate from a user’s historical baseline**.

To enable reasoning at the behavioral level, raw listening events are aggregated into **daily user-level features**, shifting the focus from individual actions to patterns over time.

The dataset used in this project is generated from **explicit behavioral assumptions**, not random noise, allowing controlled analysis and interpretability.

---

## Data Assumptions

This project does **not** use real Spotify data.

Instead, it generates a controlled synthetic dataset designed to mimic realistic listening behavior.  
Certain aspects of real-world complexity — such as device switching, network effects, or playlist context — are intentionally simplified to maintain interpretability and focus on reasoning rather than scale.

---

## Detection Approaches

Two complementary anomaly detection strategies are explored:

- A **rule-based approach**, grounded in user-specific statistical baselines  
- A **machine learning–based approach**, using Isolation Forest to learn normal behavior directly from data  

| Aspect          | Rule-Based        | ML-Based           |
|-----------------|------------------|--------------------|
| Explainability  | High             | Medium             |
| Setup Cost      | Low              | Medium             |
| Adaptability    | Low              | High               |
| Drift Handling  | Manual           | Implicit           |
| Best Use Case   | Clear violations | Emerging patterns  |

In practice, these approaches are **complementary rather than competing**.

---

## Production Considerations

In a real system, anomaly detection is not about catching *all* anomalies,  
but about catching the *right* ones.

A hybrid production setup could involve:

- Rule-based detection for clear, explainable violations  
- ML-based detection to surface novel or drifting behaviors  
- Human-in-the-loop review for high-impact decisions  

---

## Running the Pipeline

```bash
python run_pipeline.py

During our evaluation, we noticed that Rule-Based Detection is excellent at catching "obvious" violations (e.g., listening for 23 hours straight). However, it often misses subtle behavioral shifts—like a user who stays within normal time limits but starts listening exclusively to 30-second tracks at 3 AM.

The Isolation Forest model excelled at identifying these multidimensional anomalies that don't necessarily cross a single threshold but represent an "impossible" combination of features.