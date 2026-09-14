"""Comprehensive deterministic ranking quality and adaptivity test suite for Nancora pre-PyPI audit."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nancora.analysis.evidence import format_p_value, insight_for, sanitize_stats
from nancora.engine import explore


def test_score_breakdown_exact_sum():
    """Verify score == sum(score_breakdown components) for all candidates."""
    rng = np.random.RandomState(42)
    df = pd.DataFrame({
        "x": np.linspace(0, 10, 50),
        "y": np.linspace(0, 20, 50) + rng.randn(50),
        "cat": rng.choice(["A", "B"], 50),
    })
    res = explore(df)
    for cand in res.selected + res.rejected:
        if cand.score > 0 and cand.breakdown:
            sum_deltas = sum(round(item["delta"], 1) for item in cand.breakdown.items)
            assert abs(sum_deltas - cand.score) <= 0.2, (
                f"Candidate {cand.analysis_id} {cand.variables} score {cand.score} != sum {sum_deltas}"
            )


def test_scenario_01_strong_relationship():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({"x": np.linspace(0, 10, n), "y": np.linspace(0, 10, n) + rng.randn(n) * 0.01})
    res = explore(df, rng_seed=42)
    top_id = res.selected[0].analysis_id
    assert top_id in ("numeric_relationship", "correlation_analysis")
    assert res.selected[0].score >= 80.0


def test_scenario_02_weak_relationship():
    rng = np.random.RandomState(42)
    n = 100
    df_strong = pd.DataFrame({"x": np.linspace(0, 10, n), "y": np.linspace(0, 10, n) + rng.randn(n) * 0.01})
    df_weak = pd.DataFrame({"x": rng.randn(n), "y": rng.randn(n) * 0.05 + 0.1 * rng.randn(n)})
    res_strong = explore(df_strong, rng_seed=42)
    res_weak = explore(df_weak, rng_seed=42)
    rel_strong = [c for c in res_strong.selected if c.analysis_id == "numeric_relationship"][0]
    rel_weak = [c for c in res_weak.selected if c.analysis_id == "numeric_relationship"][0]
    assert rel_strong.score > rel_weak.score


def test_scenario_03_no_relationship():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({"x": rng.randn(n), "y": rng.randn(n)})
    res = explore(df, rng_seed=42)
    rel = [c for c in res.selected if c.analysis_id == "numeric_relationship"]
    if rel:
        assert rel[0].score < 82.0


def test_scenario_04_nonlinear_relationship():
    rng = np.random.RandomState(42)
    n = 100
    t = np.linspace(-3, 3, n)
    df = pd.DataFrame({"x": t, "y": t**2 + rng.randn(n) * 0.1})
    res = explore(df, rng_seed=42)
    assert len(res.selected) > 0


def test_scenario_05_high_missingness():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({"a": rng.randn(n), "b": rng.randn(n)})
    df.iloc[:40, 0] = np.nan
    res = explore(df, rng_seed=42)
    assert res.selected[0].analysis_id == "missingness_analysis"
    assert res.selected[0].score >= 75.0


def test_scenario_06_low_missingness():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({"a": rng.randn(n), "b": rng.randn(n)})
    df.iloc[:2, 0] = np.nan  # 2% missingness
    res = explore(df, rng_seed=42)
    missing_cands = [c for c in res.selected if c.analysis_id == "missingness_analysis"]
    assert len(missing_cands) > 0
    assert 55.0 <= missing_cands[0].score <= 75.0


def test_scenario_07_no_missingness():
    df = pd.DataFrame({"a": np.arange(100, dtype=float), "b": np.arange(100, dtype=float)})
    res = explore(df, rng_seed=42)
    missing_cands = [c for c in res.selected if c.analysis_id == "missingness_analysis"]
    if missing_cands:
        assert missing_cands[0].score <= 45.0
    assert "missingness_analysis" not in [c.analysis_id for c in res.selected[:2]]


def test_scenario_08_outliers():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({"a": np.concatenate([rng.randn(n - 5), [100.0, -100.0, 90.0, -90.0, 85.0]])})
    res = explore(df, rng_seed=42)
    selected_ids = [c.analysis_id for c in res.selected]
    assert "outlier_analysis" in selected_ids
    assert "numeric_distribution" in selected_ids


def test_scenario_09_no_outliers():
    df = pd.DataFrame({"col": np.linspace(-1.0, 1.0, 100)})
    res = explore(df, rng_seed=42)
    selected_ids = [c.analysis_id for c in res.selected]
    rejected_sim = [r for r in res.rejected if r.analysis_id == "outlier_analysis"]
    assert "numeric_distribution" in selected_ids
    assert len(rejected_sim) > 0


def test_scenario_10_binary_target():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({
        "target": [True] * 50 + [False] * 50,
        "score": np.concatenate([rng.normal(5, 1, 50), rng.normal(1, 1, 50)]),
    })
    res = explore(df, target="target", rng_seed=42)
    assert res.selected[0].analysis_id == "target_aware"


def test_scenario_11_categorical_target():
    rng = np.random.RandomState(42)
    n = 120
    df = pd.DataFrame({
        "segment": ["Low", "Med", "High"] * 40,
        "spend": np.concatenate([rng.normal(10, 2, 40), rng.normal(50, 5, 40), rng.normal(100, 10, 40)]),
    })
    res = explore(df, target="segment", rng_seed=42)
    selected_ids = [c.analysis_id for c in res.selected[:2]]
    assert "target_aware" in selected_ids


def test_scenario_12_imbalanced_target():
    rng = np.random.RandomState(42)
    n = 150
    df = pd.DataFrame({
        "churned": [True] * 15 + [False] * 135,
        "tenure": np.concatenate([rng.normal(3, 1, 15), rng.normal(36, 5, 135)]),
    })
    res = explore(df, target="churned", rng_seed=42)
    assert "target_aware" in [c.analysis_id for c in res.selected[:2]]


def test_scenario_13_time_trend():
    rng = np.random.RandomState(42)
    n = 100
    dates = pd.date_range("2025-01-01", periods=n, freq="D")
    df = pd.DataFrame({"date": dates, "value": np.arange(n, dtype=float) + rng.randn(n)})
    res = explore(df, rng_seed=42)
    assert "datetime_numeric_trend" in [c.analysis_id for c in res.selected[:2]]


def test_scenario_14_high_cardinality_identifier():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({"id": [f"USER_{i}" for i in range(n)], "val": rng.randn(n)})
    res = explore(df, rng_seed=42)
    assert "cardinality_analysis" in [c.analysis_id for c in res.selected]


def test_scenario_15_noisy_dataset():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({
        "n1": rng.randn(n),
        "n2": rng.randn(n),
        "n3": rng.randn(n),
        "c1": rng.choice(["A", "B", "C"], n),
    })
    res = explore(df, rng_seed=42)
    assert len(res.selected) <= 10
    # No single analysis should artificially blow up to 95+ score on pure noise
    assert max(c.score for c in res.selected) < 85.0


def test_package_version():
    import nancora

    assert hasattr(nancora, "__version__")
    assert nancora.__version__ == "0.1.1"

