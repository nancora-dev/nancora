import numpy as np
import pandas as pd
import pytest

import nancora as nc
from nancora.exceptions import AnalysisError


def test_edge_case_empty_dataframe():
    with pytest.raises(AnalysisError, match="empty DataFrame"):
        nc.explore(pd.DataFrame())


def test_edge_case_invalid_target():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})
    with pytest.raises(AnalysisError, match="Target column not found"):
        nc.analyze(df, target="non_existent_column")


def test_edge_case_single_row():
    df = pd.DataFrame({"x": [1.0], "y": [2.0], "cat": ["a"]})
    res = nc.explore(df)
    assert res.summary()["n_rows"] == 1
    assert isinstance(res.recommendations(), list)


def test_edge_case_single_column():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
    res = nc.explore(df)
    assert res.summary()["n_cols"] == 1
    assert any(c.analysis_id == "numeric_distribution" for c in res.selected)


def test_edge_case_duplicate_column_names():
    df = pd.DataFrame([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], columns=["x", "x", "y"])
    res = nc.explore(df)
    assert "x" in [c.name for c in res.dataset_profile.columns]
    assert "x_1" in [c.name for c in res.dataset_profile.columns]


def test_edge_case_infinite_and_null_values():
    df = pd.DataFrame(
        {
            "x": [1.0, np.inf, 3.0, -np.inf, np.nan, 6.0, 7.0, 8.0],
            "y": [2.0, 4.0, np.nan, 8.0, 10.0, 12.0, 14.0, 16.0],
        }
    )
    res = nc.explore(df)
    assert res.summary()["n_rows"] == 8
    num_cand = next(c for c in res.selected if c.analysis_id == "numeric_distribution")
    assert num_cand.evidence is not None
    assert num_cand.evidence.stats["n"] == 5.0  # 5 finite values (excluding inf, -inf, nan)


def test_edge_case_non_string_column_names():
    df = pd.DataFrame([[1, 2], [3, 4]], columns=[10, 20])
    res = nc.explore(df)
    assert "10" in [c.name for c in res.dataset_profile.columns]
    assert "20" in [c.name for c in res.dataset_profile.columns]


def test_golden_dataset_linear_relationship():
    n = 50
    rng = np.random.default_rng(42)
    x = rng.normal(size=n)
    y = x * 4.5 + rng.normal(scale=0.1, size=n)
    noise = rng.normal(size=n)
    df = pd.DataFrame({"x": x, "y": y, "noise": noise})

    res = nc.explore(df, max_analyses=5)
    rec_ids = [c.analysis_id for c in res.selected]

    assert "numeric_relationship" in rec_ids or "correlation_analysis" in rec_ids
    cand = next(c for c in res.selected if c.analysis_id == "numeric_relationship")
    assert cand.evidence is not None
    assert cand.evidence.stats["coefficient"] > 0.95


def test_golden_dataset_target_analysis():
    n = 60
    rng = np.random.default_rng(42)
    feature = rng.normal(size=n)
    target = feature * 2.0 + rng.normal(scale=0.2, size=n)
    df = pd.DataFrame({"feat": feature, "target": target, "noise": rng.normal(size=n)})

    res = nc.analyze(df, target="target", max_analyses=5)
    rec_ids = [c.analysis_id for c in res.selected]
    assert "target_aware" in rec_ids
    target_cand = next(c for c in res.selected if c.analysis_id == "target_aware")
    assert target_cand.score >= 70.0
