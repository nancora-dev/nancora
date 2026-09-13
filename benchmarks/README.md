# Benchmarks

This directory is a **framework**, not a published leaderboard.

- `datasets/` — tiny synthetic CSVs committed with the repo
- `labels/` — optional human labels (`useful`, `essential`, `redundant`, `irrelevant`, `misleading`)
- `runner.py` — runs `explore` and computes metrics **only when labels exist**
- `metrics.py` — precision@k, essential recall, redundancy reduction, coverage, runtime, information efficiency

Empty `labels` arrays mean the runner prints `no labels; skip scoring`. Do not fabricate results.
