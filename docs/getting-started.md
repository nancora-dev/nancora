# Getting Started

Nancora helps answer: *"Which analyses should I perform on this dataset, and why?"*

```python
import nancora as nc

# Load dataset
df = nc.read_csv("data.csv")

# 1. Unsupervised exploration
result = nc.explore(df)

# 2. Target-aware exploration
result = nc.explore(df, target="churn")

# Jupyter Notebook Experience: Simply evaluate `result` for clean HTML rendering!

# Access clean structured properties
print("Profile:", result.profile.n_rows, "rows,", result.profile.n_cols, "columns")

print("\nTop Recommendations:")
for rec in result.recommendations:
    print(f"- {rec.analysis_id} ({rec.variables}): score={rec.score}")
    print(f"  Explanation: {rec.explanation}")

print("\nKey Insights:")
for insight in result.insights:
    print(f"- {insight}")

# Save full static HTML report
result.save("report.html")
```

CLI:
```bash
nancora explore data.csv --out report.html
nancora analyze data.csv --target churn --out report.html
```
