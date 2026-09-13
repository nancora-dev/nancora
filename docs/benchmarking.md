# Benchmarking

`benchmarks/runner.py` loads synthetic datasets and optional human labels.

Label values: `useful`, `essential`, `redundant`, `irrelevant`, `misleading`.

If a dataset has no labels, the runner **skips metrics** rather than inventing scores. Do not commit fabricated precision/recall.
