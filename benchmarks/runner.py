"""Run labeled recommendation checks. Skips metrics when labels are absent."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nancora.engine import explore  # noqa: E402
from nancora.types import RejectReason  # noqa: E402

from benchmarks.metrics import (  # noqa: E402
    coverage_of_essential,
    information_efficiency,
    precision_at_k,
    recall_essential,
    redundancy_reduction,
)

LABELS_DIR = Path(__file__).parent / "labels"
DATA_DIR = Path(__file__).parent / "datasets"
REDUNDANT_REASONS = {
    RejectReason.EXACT_DUPLICATE.value,
    RejectReason.SYMMETRIC_DUPLICATE.value,
    RejectReason.SIMILAR_ANALYSIS.value,
    RejectReason.COVERAGE_OVERLAP.value,
    RejectReason.DOMINATED.value,
}


def _key(analysis_id: str, variables: list[str] | tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
    return analysis_id, tuple(sorted(variables))


def load_labels(dataset_id: str) -> list[dict]:
    path = LABELS_DIR / f"{dataset_id}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("labels") or [])


def run_dataset(csv_path: Path) -> dict:
    dataset_id = csv_path.stem
    labels = load_labels(dataset_id)
    df = pd.read_csv(csv_path)
    started = time.perf_counter()
    result = explore(df, max_analyses=10, rng_seed=0)
    runtime = time.perf_counter() - started
    selected = [_key(c.analysis_id, c.variables) for c in result.selected]
    report = {
        "dataset_id": dataset_id,
        "runtime_seconds": round(runtime, 6),
        "n_selected": len(result.selected),
        "n_rejected": len(result.rejected),
        "labels_present": bool(labels),
    }
    if not labels:
        report["metrics"] = None
        report["note"] = "no labels; skip scoring"
        return report

    by_kind: dict[str, set] = {k: set() for k in ("useful", "essential", "redundant", "irrelevant", "misleading")}
    for row in labels:
        by_kind.setdefault(row["kind"], set()).add(_key(row["analysis_id"], row["variables"]))

    n_pairs = sum(1 for c in result.selected + result.rejected if len(c.variables) == 2)
    n_red = sum(
        1
        for c in result.rejected
        if c.reject_reason and c.reject_reason.value in REDUNDANT_REASONS
    )
    useful = by_kind["useful"] | by_kind["essential"]
    report["metrics"] = {
        "precision_at_5": precision_at_k(selected, useful, 5),
        "recall_essential": recall_essential(selected, by_kind["essential"]),
        "redundancy_reduction": redundancy_reduction(n_pairs, n_red),
        "analytical_coverage": coverage_of_essential(selected, by_kind["essential"]),
        "information_efficiency": information_efficiency(selected),
        "runtime_seconds": round(runtime, 6),
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Nancora benchmark runner")
    parser.parse_args(argv)
    datasets = sorted(DATA_DIR.glob("*.csv"))
    if not datasets:
        print("no datasets found")
        return 0
    for path in datasets:
        print(json.dumps(run_dataset(path), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
