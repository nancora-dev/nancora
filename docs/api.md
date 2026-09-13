# Public API

```python
import nancora as nc

nc.read_csv / read_excel / read_json / read_parquet
nc.explore(df, max_analyses=10, rng_seed=0)
nc.analyze(df, target=..., max_analyses=10, rng_seed=0)
nc.register_analysis
nc.list_analyses()
nc.get_analysis(id)

nc.data / nc.numpy / nc.stats / nc.plot / nc.analysis
```

`AnalysisResult`: `summary`, `profile`, `recommendations`, `insights`, `rejected`, `visualize`, `to_dict`, `to_json`, `save`.
