# Contributing

Nancora must not become a pile of unrelated wrappers.

Every public feature should either:

1. provide a curated data-science abstraction the engine uses, or
2. strengthen recommendation, scoring, redundancy, or explainability.

Do not reimplement Pandas, NumPy, SciPy, Matplotlib, or Plotly.
Do not invent statistical evidence or causal claims from association.
Do not add APIs merely to increase surface area.

## Setup

```bash
python -m pip install -e ".[dev]"
pytest
ruff check src tests
```

New analyses register with `@nancora.register_analysis` and implement `propose`, `compute_evidence`, and `plot_spec`. Add a decision test when ranking behavior changes.
