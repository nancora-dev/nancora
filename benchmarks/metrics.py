"""Benchmark metrics. Computed only from labels — never fabricated."""

from __future__ import annotations

from typing import Any


def precision_at_k(selected: list[tuple[str, tuple[str, ...]]], useful: set[tuple[str, tuple[str, ...]]], k: int) -> float | None:
    if not useful:
        return None
    top = selected[:k]
    if not top:
        return 0.0
    hits = sum(1 for item in top if item in useful)
    return hits / len(top)


def recall_essential(
    selected: list[tuple[str, tuple[str, ...]]], essential: set[tuple[str, tuple[str, ...]]]
) -> float | None:
    if not essential:
        return None
    hits = sum(1 for item in essential if item in set(selected))
    return hits / len(essential)


def redundancy_reduction(n_generated_pairs: int, n_rejected_redundant: int) -> float | None:
    if n_generated_pairs <= 0:
        return None
    return n_rejected_redundant / n_generated_pairs


def coverage_of_essential(
    selected: list[tuple[str, tuple[str, ...]]], essential: set[tuple[str, tuple[str, ...]]]
) -> float | None:
    return recall_essential(selected, essential)


def information_efficiency(selected: list[tuple[str, tuple[str, ...]]]) -> float | None:
    if not selected:
        return None
    units = {(aid, var) for aid, vars_ in selected for var in vars_}
    return len(units) / len(selected)


import json
from pathlib import Path


def load_labels(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    payload = json.loads(p.read_text(encoding="utf-8"))
    return list(payload.get("labels") or [])


def evaluate_labels(labels: list[dict], data_dir: str | Path) -> dict[str, Any]:
    if not labels:
        return {"status": "no_labels"}
    return {"status": "ok"}


def summarize_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    return payload

