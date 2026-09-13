# Benchmarks

The benchmark system measures whether Nancora recommends analyses that humans marked as useful.

It does **not** ship fabricated leaderboard numbers.

## Layout

- `datasets/` — tiny, license-clean tables
- `labels/` — JSON labels (`useful`, `essential`, `redundant`, `irrelevant`, `misleading`)
- `metrics.py` — precision@k, essential recall, redundancy rejected count, runtime
- `runner.py` — prints `no labels; skip scoring` when `labels` is empty

## Label schema

```json
{
  "dataset_id": "tiny",
  "analysis_id": "numeric_relationship",
  "variables": ["spend", "revenue"],
  "label": "essential"
}
```

Add labels only from human review. Then run:

```bash
python benchmarks/runner.py
```
