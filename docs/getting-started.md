# Getting started

```bash
pip install -e ".[dev]"
```

```python
import nancora as nc

df = nc.read_csv("benchmarks/datasets/tiny.csv")
result = nc.explore(df)
print(result.summary())
for rec in result.recommendations():
    print(rec.score, rec.analysis_id, rec.variables)
    print(rec.explanation)
result.save("report.html")
```

CLI:

```bash
nancora explore benchmarks/datasets/tiny.csv --out report.html
```
