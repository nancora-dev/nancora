# Contributing

1. Keep the public API small (`explore`, `analyze`, curated `data` / `numpy` / `stats` / `plot`).
2. Do not reimplement Pandas, NumPy, SciPy, Matplotlib, or Plotly. Delegate.
3. New public functions must either feed the recommendation engine or be IO/profile helpers it uses.
4. Never fabricate statistics or causal claims.
5. Ranking scores must stay explainable heuristics.
6. Run `pytest` and `ruff check src tests benchmarks` before opening a PR.
7. Add decision tests when changing scoring or redundancy.

To register a future analysis:

```python
import nancora as nc

@nc.register_analysis
class MyAnalysis:
    id = "my_analysis"
    ...
```

There is no plugin marketplace in this version.
