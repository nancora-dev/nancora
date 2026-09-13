# Quickstart — Nancora Python Library

Get started with Nancora in under two minutes.

## 1. Unsupervised Exploration

Use `nancora.explore()` to discover the most informative analytical directions in a pandas DataFrame:

```python
import pandas as pd
import nancora as nc

df = pd.DataFrame({
    "age": [20, 25, 45, 50, 60],
    "income": [24000, 31000, 78000, 85000, 99000],
    "city": ["Surat", "Surat", "Mumbai", "Delhi", "Mumbai"],
})

# Explore dataset
result = nc.explore(df)

# Print top recommendations
for rec in result.recommendations[:3]:
    print(f"[{rec.score:.1f}] {rec.analysis_id} on {rec.variables}")
```

## 2. Target-Aware Exploration

Focus recommendations on a specific variable of interest (e.g., customer churn):

```python
result = nc.explore(df, target="income")

# Print top target-focused recommendations
for rec in result.recommendations[:3]:
    print(f"[{rec.score:.1f}] {rec.analysis_id} on {rec.variables}")
```

## 3. Serialization and HTML Reports

Export results to JSON or save self-contained HTML reports:

```python
# Convert to dictionary or JSON
dict_data = result.to_dict()
json_string = result.to_json(indent=2)

# Save static HTML report
result.save("report.html")
```
