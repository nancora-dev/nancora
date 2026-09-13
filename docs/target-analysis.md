# Target analysis

```python
result = nc.analyze(df, target="y")
```

`target_aware` proposes:

- target distribution
- target vs numeric features
- target vs categorical features

Target membership also boosts heuristic relevance for any candidate that includes the target column.
