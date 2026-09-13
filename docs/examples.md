# Practical Examples — Nancora Python Library

Real-world code snippets demonstrating Nancora usage patterns.

## 1. Unsupervised Exploration Example

```python
import pandas as pd
import nancora as nc

df = pd.DataFrame({
    "tenure": [1, 12, 24, 36, 48, 60],
    "monthly_charges": [30.0, 65.0, 80.0, 95.0, 105.0, 115.0],
    "contract": ["month", "one-year", "two-year", "one-year", "two-year", "two-year"],
})

result = nc.explore(df)

print("Top Recommendations:")
for rec in result.recommendations:
    print(f"- {rec.analysis_id} on {rec.variables} (Score: {rec.score:.1f})")
```

## 2. Customer Churn Target-Aware Example

```python
import pandas as pd
import nancora as nc

df = pd.DataFrame({
    "tenure": [1, 12, 24, 36, 48, 60],
    "monthly_charges": [30.0, 65.0, 80.0, 95.0, 105.0, 115.0],
    "churn": ["yes", "yes", "no", "no", "no", "no"],
})

result = nc.analyze(df, target="churn")
result.save("churn_report.html")
print("Saved churn exploration report.")
```

## 3. Custom Script Execution

Run pre-packaged examples from the repository:

```bash
python examples/basic_exploration.py
python examples/target_analysis.py
python examples/file_loading.py
```
