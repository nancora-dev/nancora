# Tutorials — Nancora Python Library

Step-by-step guides for conducting data analysis with Nancora.

## Tutorial 1: Profiling a New Dataset

When starting a project with a new dataset, follow this 4-step workflow:

### Step 1: Load your dataset

```python
import nancora as nc

df = nc.read_csv("dataset.csv")
```

### Step 2: Run unsupervised exploration

```python
result = nc.explore(df)
```

### Step 3: Inspect natural language evidence insights

```python
for insight in result.insights:
    print(f"• {insight}")
```

### Step 4: Export report for team sharing

```python
result.save("dataset_exploration.html")
```

---

## Tutorial 2: Target Variable Screening

When analyzing feature relationships against a target outcome (e.g. sales, churn, fraud):

```python
result = nc.analyze(df, target="target_column")

# Review decision trace
trace = result.decision_trace
print("Top Scores:", trace["summary"]["top_scores"])
```
