"""Benchmark metrics. Computed only when human labels exist. Never fabricate results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

import nancora as nc

VALID_LABELS = {"useful", "essential", "redundant", "irrelevant", "misleading"}


def load_labels(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("labels", [])
    if not records:
        return []
    return records


def _candidate_key(analysis_id: str, variables: list[str]) -> tuple[str, tuple[str, ...]]:
    return analysis_id, tuple(sorted(variables))


def evaluate_labels(labels: list[dict[str, Any]], datasets_dir: Path) -> dict[str, Any]:
    """Evaluate recommendations against human labels. Returns metrics only for labeled datasets."""
    if not labels:
        return {"status": "no_labels"}

    by_dataset: dict[str, list[dict[str, Any]]] = {}
    for row in labels:
        by_dataset.setdefault(row["dataset_id"], []).append(row)

    reports = []
    for dataset_id, rows in sorted(by_dataset.items()):
        csv_path = datasets_dir / f"{dataset_id}.csv"
        if not csv_path.exists():
            reports.append({"dataset_id": dataset_id, "error": "dataset_missing"})
            continue
        df = pd.read_csv(csv_path)
        result = nc.explore(df)
        selected = {
            _candidate_key(c.analysis_id, list(c.variables)) for c in result.recommendations()
        }
        essential = {
            _candidate_key(r["analysis_id"], r["variables"])
            for r in rows
            if r.get("label") == "essential"
        }
        useful = {
            _candidate_key(r["analysis_id"], r["variables"])
            for r in rows
            if r.get("label") in {"essential", "useful"}
        }
        tp = len(selected & useful)
        precision = tp / len(selected) if selected else 0.0
        recall_essential = (len(selected & essential) / len(essential)) if essential else None
        rejected_redundancy = [
            c
            for c in result.rejected()
            if c.reject_reason and c.reject_reason.value
            in {"exact_duplicate", "symmetric_duplicate", "similar_analysis"}
        ]
        reports.append(
            {
                "dataset_id": dataset_id,
                "precision_at_k": round(precision, 4),
                "recall_essential": None if recall_essential is None else round(recall_essential, 4),
                "n_selected": len(selected),
                "n_essential_labels": len(essential),
                "redundancy_rejected": len(rejected_redundancy),
                "runtime_seconds": result.timings().get("pipeline_seconds"),
            }
        )
    return {"status": "ok", "datasets": reports}
