"""Benchmark runner. Does not fabricate scores when labels are missing."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from metrics import evaluate_labels, load_labels  # noqa: E402


def main() -> None:
    labels_path = ROOT / "labels" / "example.json"
    labels = load_labels(labels_path)
    if not labels:
        print("no labels; skip scoring")
        return
    metrics = evaluate_labels(labels, ROOT / "datasets")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
