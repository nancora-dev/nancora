# Nancora

Nancora is a Python toolkit for tabular data science. It loads and profiles data with Pandas, computes statistics with NumPy and SciPy, and draws charts with Matplotlib or Plotly.

The product is not another plotting wrapper. **Nancora ranks which analyses are worth attention**, with an explainable heuristic score, redundancy filtering, and machine-readable results.

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
result = nc.analyze(df, target="target", max_analyses=10)
```

## What this is not

- Not an LLM chatbot
- Not AutoML
- Not a replacement for Pandas, NumPy, SciPy, Matplotlib, or Plotly
- Ranking scores are **heuristics**, not scientific truth
- Association is **not** causation

See [LIMITATIONS.md](LIMITATIONS.md), [PHASES.md](PHASES.md), and `docs/`.

## Install (development)

```bash
pip install -e ".[dev]"
pytest
```

Excel and Parquet extras: `pip install -e ".[excel,parquet]"`.

## CLI

```bash
nancora explore data.csv --target y --max-analyses 10 --out report.html
```
