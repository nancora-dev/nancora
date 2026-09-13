# Nancora

Nancora is a Python data-science toolkit that **recommends which analyses are worth attention**.

It does not reimplement Pandas, NumPy, SciPy, Matplotlib, or Plotly. Those libraries do the computation. Nancora profiles data, generates analysis candidates, scores them with an **explainable heuristic**, removes redundant work, and returns a machine-readable result plus an HTML report.

```python
import nancora as nc

df = nc.read_csv("data.csv")
result = nc.explore(df)
result.summary()
result.recommendations()
result.insights()
result.visualize()
result.save("report.html")
```

Target-aware path:

```python
result = nc.analyze(df, target="y", max_analyses=10)
```

Scores are ranking heuristics (0–100), not scientific truth. Association is not causation.

## Install

```bash
pip install -e ".[dev]"
```

Excel and Parquet extras: `nancora[excel]`, `nancora[parquet]`.

## CLI

```bash
nancora explore data.csv --out report.html
nancora analyze data.csv --target y --out report.html
```

## What Nancora is not

No LLM chatbot, AutoML, cloud platform, plugin marketplace, or deep-learning stack. See [LIMITATIONS.md](LIMITATIONS.md) and [docs/architecture.md](docs/architecture.md).
