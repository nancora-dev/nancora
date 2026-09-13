# Configuration — Nancora Python Library

Nancora provides simple, explicit configuration parameters for pipeline exploration.

## Exploration Parameters

### `max_analyses` (*int*, default: `10`)

Controls the maximum number of top-ranked candidate recommendations returned in `result.selected` / `result.recommendations`.

```python
result = nc.explore(df, max_analyses=5)
```

Must be a positive integer (`max_analyses >= 1`). Passing `0` or negative values raises `ConfigurationError`.

### `target` (*str | None*, default: `None`)

Designates a primary column of interest for target-aware exploration.

```python
result = nc.explore(df, target="churn_status")
```

When specified:
- Candidate analyses involving the target column receive a $+14.0$ proximity boost.
- Target-aware bivariate and group comparison candidates are generated.

### `rng_seed` (*int*, default: `0`)

Random number generator seed used for deterministic tie-breaking during ranking.

```python
result = nc.explore(df, rng_seed=42)
```
