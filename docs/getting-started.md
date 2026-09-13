# Getting started

```python
import nancora as nc

df = nc.read_csv("data.csv")
result = nc.explore(df)
print(result.summary())
for rec in result.recommendations():
    print(rec.analysis_id, rec.variables, rec.score)
    print(rec.explanation)
result.save("report.html")
```

With a target:

```python
result = nc.analyze(df, target="churn", max_analyses=10)
```

CLI: `nancora explore data.csv --out report.html`
