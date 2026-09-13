"""Regression test suite for Nancora recommendation intelligence and adaptivity."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nancora.analysis.evidence import format_p_value, insight_for, sanitize_stats
from nancora.engine import explore


def test_issue1_zero_vs_high_missingness():
    # 0% missingness dataset
    df_clean = pd.DataFrame(
        {
            "a": np.arange(100, dtype=float),
            "b": np.arange(100, dtype=float) * 2.0,
            "c": np.random.RandomState(42).randn(100),
        }
    )
    res_clean = explore(df_clean)
    missing_cands_clean = [c for c in res_clean.selected if c.analysis_id == "missingness_analysis"]
    if missing_cands_clean:
        assert missing_cands_clean[0].score <= 45.0, f"0% missingness score should be low, got {missing_cands_clean[0].score}"

    # High missingness dataset (30% missing cells)
    df_missing = df_clean.copy()
    rng = np.random.RandomState(42)
    mask = rng.rand(*df_missing.shape) < 0.3
    df_missing[mask] = np.nan
    res_missing = explore(df_missing)
    missing_cands = [c for c in res_missing.selected if c.analysis_id == "missingness_analysis"]
    assert len(missing_cands) > 0
    assert missing_cands[0].score >= 70.0, f"High missingness score should be high, got {missing_cands[0].score}"


def test_issue2_outlier_vs_distribution_redundancy():
    # Bounded dataset with zero IQR outliers (linspace -1 to 1)
    df_zero_outliers = pd.DataFrame({"col": np.linspace(-1.0, 1.0, 100)})
    res_zero = explore(df_zero_outliers)
    selected_ids = [c.analysis_id for c in res_zero.selected]
    rejected_sim = [r for r in res_zero.rejected if r.analysis_id == "outlier_analysis"]
    assert "numeric_distribution" in selected_ids
    assert len(rejected_sim) > 0, "Outlier analysis with 0 outliers should be rejected as redundant"

    # Dataset with strong outliers
    rng = np.random.RandomState(42)
    df_outliers = pd.DataFrame({"col": np.concatenate([rng.randn(90), [50.0, 100.0, -80.0]])})
    res_outliers = explore(df_outliers)
    selected_outliers_ids = [c.analysis_id for c in res_outliers.selected]
    assert "numeric_distribution" in selected_outliers_ids
    assert "outlier_analysis" in selected_outliers_ids, "Outlier analysis with positive outliers should be selected alongside numeric_distribution"


def test_issue3_extremely_small_p_values():
    assert format_p_value(0.0) == "< 1e-12"
    assert format_p_value(1e-15) == "< 1e-12"
    assert format_p_value(1.23e-5) == "1.23e-05"
    assert format_p_value(0.0456) == "0.0456"

    # Sanitize stats preserves exact float p_value without rounding to 0.0
    stats = {"p_value": 1.2345e-18, "statistic": 105.4}
    san = sanitize_stats(stats)
    assert san["p_value"] == 1.2345e-18
    assert san["p_value_display"] == "< 1e-12"

    # Test strong group difference produce p_value_display without literal zero
    rng = np.random.RandomState(42)
    g1 = rng.randn(500)
    g2 = rng.randn(500) + 10.0
    df = pd.DataFrame({"group": ["A"] * 500 + ["B"] * 500, "val": np.concatenate([g1, g2])})
    res = explore(df)
    cat_num = [c for c in res.selected if c.analysis_id == "categorical_numeric"][0]
    p_val = cat_num.evidence.stats.get("p_value")
    p_disp = cat_num.evidence.stats.get("p_value_display")
    assert p_val is not None
    assert p_disp == "< 1e-12"
    assert "p=< 1e-12" in insight_for(cat_num)


def test_issue4_boolean_targets():
    rng = np.random.RandomState(42)
    n = 200
    churned = rng.rand(n) > 0.7  # imbalanced boolean target
    age = np.where(churned, rng.normal(50, 5, n), rng.normal(30, 5, n))  # numeric diff by target
    tier = np.where(churned, rng.choice(["Basic", "Free"], n), rng.choice(["Premium", "Enterprise"], n))  # cat diff

    df = pd.DataFrame({"churned": churned, "age": age, "tier": tier})

    res = explore(df, target="churned")
    selected_target_views = [c for c in res.selected if c.analysis_id == "target_aware"]
    assert len(selected_target_views) >= 2, "Should recommend target-aware views for boolean target"

    vars_involved = [c.variables for c in selected_target_views]
    assert any("churned" in v and "age" in v for v in vars_involved)
    assert any("churned" in v and "tier" in v for v in vars_involved)


def test_issue6_dataset_adaptivity_14_scenarios():
    rng = np.random.RandomState(42)
    n = 150

    # 1. Strong linear relationship
    df1 = pd.DataFrame({"x": np.linspace(0, 10, n), "y": np.linspace(0, 10, n) + rng.randn(n) * 0.1})
    res1 = explore(df1)
    assert any(c.analysis_id in ("numeric_relationship", "correlation_analysis") for c in res1.selected[:2])

    # 2. Weak relationship
    df2 = pd.DataFrame({"x": rng.randn(n), "y": rng.randn(n) * 0.05 + 0.1 * rng.randn(n)})
    res2 = explore(df2)
    rel2 = [c for c in res2.selected if c.analysis_id == "numeric_relationship"]
    rel1 = [c for c in res1.selected if c.analysis_id == "numeric_relationship"]
    if rel1 and rel2:
        assert rel1[0].score > rel2[0].score

    # 3. No relationship
    df3 = pd.DataFrame({"x": rng.randn(n), "y": rng.randn(n)})
    res3 = explore(df3)
    assert res3.selected[0].score < 80.0

    # 4. Nonlinear relationship
    t = np.linspace(-3, 3, n)
    df4 = pd.DataFrame({"x": t, "y": t**2 + rng.randn(n) * 0.1})
    res4 = explore(df4)
    assert len(res4.selected) > 0

    # 5. Strong outliers
    df5 = pd.DataFrame({"a": np.concatenate([rng.randn(n - 5), [100.0, -100.0, 90.0, -90.0, 85.0]])})
    res5 = explore(df5)
    assert "outlier_analysis" in [c.analysis_id for c in res5.selected]

    # 6. High missingness
    df6 = pd.DataFrame({"a": rng.randn(n), "b": rng.randn(n)})
    df6.iloc[:60, 0] = np.nan
    res6 = explore(df6)
    assert res6.selected[0].analysis_id == "missingness_analysis"

    # 7. No missingness
    df7 = pd.DataFrame({"a": rng.randn(n), "b": rng.randn(n)})
    res7 = explore(df7)
    assert "missingness_analysis" not in [c.analysis_id for c in res7.selected[:2]]

    # 8. Strong categorical group differences
    df8 = pd.DataFrame({
        "group": ["A"] * 75 + ["B"] * 75,
        "val": np.concatenate([rng.normal(0, 1, 75), rng.normal(10, 1, 75)]),
    })
    res8 = explore(df8)
    assert "categorical_numeric" in [c.analysis_id for c in res8.selected[:2]]

    # 9. No meaningful group differences
    df9 = pd.DataFrame({
        "group": ["A"] * 75 + ["B"] * 75,
        "val": rng.randn(150),
    })
    res9 = explore(df9)
    cn8 = [c for c in res8.selected if c.analysis_id == "categorical_numeric"]
    cn9 = [c for c in res9.selected if c.analysis_id == "categorical_numeric"]
    if cn8 and cn9:
        assert cn8[0].score > cn9[0].score

    # 10. Time trend
    dates = pd.date_range("2025-01-01", periods=n, freq="D")
    df10 = pd.DataFrame({"date": dates, "value": np.arange(n, dtype=float) + rng.randn(n)})
    res10 = explore(df10)
    assert "datetime_numeric_trend" in [c.analysis_id for c in res10.selected[:2]]

    # 11. Binary target
    df11 = pd.DataFrame({
        "target": [True] * 75 + [False] * 75,
        "score": np.concatenate([rng.normal(5, 1, 75), rng.normal(1, 1, 75)]),
    })
    res11 = explore(df11, target="target")
    assert "target_aware" in [c.analysis_id for c in res11.selected[:2]]

    # 12. Imbalanced binary target
    df12 = pd.DataFrame({
        "target": [True] * 15 + [False] * 135,
        "score": np.concatenate([rng.normal(5, 1, 15), rng.normal(1, 1, 135)]),
    })
    res12 = explore(df12, target="target")
    assert "target_aware" in [c.analysis_id for c in res12.selected[:2]]

    # 13. High-cardinality ID
    df13 = pd.DataFrame({
        "id": [f"ID_{i}" for i in range(n)],
        "val": rng.randn(n),
    })
    res13 = explore(df13)
    assert "cardinality_analysis" in [c.analysis_id for c in res13.selected]

    # 14. Constant columns
    df14 = pd.DataFrame({"const": [1.0] * n, "val": rng.randn(n)})
    res14 = explore(df14)
    # const column should be excluded from univariate/bivariate feature analyses
    for c in res14.selected:
        if c.analysis_id in ("numeric_distribution", "numeric_relationship"):
            assert "const" not in c.variables
