"""Regression tests for determinism, score breakdown consistency, variable candidate counts, and redundancy pruning."""

import json
import pandas as pd
import nancora as nc


def sample_df():
    return pd.DataFrame({
        "x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        "y": [2.0, 4.1, 6.0, 8.2, 9.9, 12.1, 14.0, 16.2],
        "group": ["a", "a", "b", "b", "a", "a", "b", "b"],
    })


def test_determinism_across_runs():
    df = sample_df()
    res1 = nc.explore(df)
    res2 = nc.explore(df)

    assert res1.to_json() == res2.to_json()
    assert [c.score for c in res1.recommendations] == [c.score for c in res2.recommendations]
    assert [c.variables for c in res1.recommendations] == [c.variables for c in res2.recommendations]


def test_score_breakdown_sum():
    df = sample_df()
    res = nc.explore(df, target="y")
    for cand in res.recommendations:
        if cand.breakdown:
            calculated_sum = sum(item["delta"] for item in cand.breakdown.items)
            clamped_expected = max(0.0, min(100.0, round(calculated_sum, 1)))
            assert abs(cand.score - clamped_expected) <= 0.1, (
                f"Candidate {cand.analysis_id} score {cand.score} != breakdown sum {clamped_expected}"
            )


def test_small_dataset_produces_fewer_than_max_selected():
    # Only 1 numeric column with 4 rows -> cannot form pairs or categorical comparisons
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})
    res = nc.explore(df, max_analyses=10)
    assert len(res.recommendations) < 10
    # Should only produce numeric_distribution, missingness_analysis, outlier_analysis, cardinality_analysis
    selected_ids = [c.analysis_id for c in res.recommendations]
    assert "numeric_relationship" not in selected_ids
    assert "categorical_numeric" not in selected_ids


def test_symmetric_redundancy_pruning():
    df = sample_df()
    res = nc.explore(df)
    rejected_reasons = {r.analysis_id: r.reject_reason.value for r in res.rejected_candidates if r.reject_reason}
    # Symmetric pairs or exact duplicates should be pruned with explicit reason
    assert "symmetric_duplicate" in rejected_reasons.values() or "exact_duplicate" in rejected_reasons.values()
