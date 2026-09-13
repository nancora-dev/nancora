# Public API

```python
import nancora as nc

nc.read_csv / read_json / read_excel / read_parquet
nc.explore(df, max_analyses=10)
nc.analyze(df, target="y", max_analyses=10)
nc.profile(df)
nc.list_analyses()
nc.register_analysis
nc.data, nc.numpy, nc.stats, nc.plot, nc.analysis
```

`AnalysisResult` methods: `summary`, `profile`, `recommendations`, `insights`, `rejected`, `visualize`, `to_dict`, `to_json`, `save`.
