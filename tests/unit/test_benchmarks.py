from pathlib import Path

from benchmarks.metrics import evaluate_labels, load_labels


def test_empty_labels_skip():
    path = Path(__file__).resolve().parents[1] / "benchmarks" / "labels" / "example.json"
    labels = load_labels(path)
    assert labels == []
    assert evaluate_labels(labels, path.parent.parent / "datasets")["status"] == "no_labels"
