# Nancora

Nancora is a Python data-science toolkit that **recommends which analyses are worth attention**.

It does not reimplement Pandas, NumPy, SciPy, Matplotlib, or Plotly. Those libraries do the computation. Nancora profiles data, generates analysis candidates, scores them with an **explainable heuristic**, removes redundant work, and returns a machine-readable result plus an HTML report.

```python
import nancora as nc

df = nc.read_csv("data.csv")

# 1. Unsupervised exploration
result = nc.explore(df)

# 2. Target-aware exploration
result = nc.explore(df, target="target_column")

# Jupyter Notebook Experience: Simply evaluate `result` for clean, rich HTML rendering!

# 3. Clean structured properties
result.profile          # Dataset shape, column kinds, quality stats
result.recommendations  # Prioritized list of top analytical recommendations
result.insights         # Human-readable insights from key evidence
result.visualizations   # Matplotlib figures for top recommendations
result.decision_trace   # Complete explanation of selected & skipped analyses

# 4. Useful serialization
result.to_dict()
result.to_json()
result.save("report.html")
```

Nancora follows a strict philosophy: **SELECT → PRIORITIZE → EXPLAIN → VISUALIZE** (not flood the user with unnecessary charts).
Scores are ranking heuristics (0–100), not scientific truth. Association is not causation.

## Install

```bash
pip install nancora
```

For development installation:

```bash
pip install -e ".[dev]"
```

## CLI

```bash
nancora explore data.csv --out report.html
nancora analyze data.csv --target y --out report.html
```

## What Nancora is not

No LLM chatbot, AutoML, cloud platform, plugin marketplace, or deep-learning stack. See [LIMITATIONS.md](LIMITATIONS.md) and [docs/architecture.md](docs/architecture.md).
