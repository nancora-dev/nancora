"""Regression tests for determinism, score breakdown consistency, variable candidate counts, and redundancy pruning."""

import pandas as pd
import nancora as nc
from nancora.engine.redundancy import apply_redundancy
from nancora.analysis.base import AnalysisCandidate, AnalysisRequirements
from nancora.types import AnalysisStatus, ColumnKind, RejectReason


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

    d1 = res1.to_dict()
    d2 = res2.to_dict()
    # Timings differ slightly per CPU execution run; everything else is 100% deterministic
    d1.pop("timings", None)
    d2.pop("timings", None)
    if "summary" in d1:
        d1["summary"].pop("runtime_seconds", None)
    if "summary" in d2:
        d2["summary"].pop("runtime_seconds", None)

    assert d1 == d2
    assert [c.score for c in res1.recommendations] == [c.score for c in res2.recommendations]
    assert [c.variables for c in res1.recommendations] == [c.variables for c in res2.recommendations]


def test_score_breakdown_sum():
    df = sample_df()
    res = nc.explore(df, target="y")
    for cand in res.recommendations:
        if cand.breakdown:
            calculated_sum = sum(item["delta"] for item in cand.breakdown.items)
            clamped_expected = max(0.0, min(100.0, round(calculated_sum, 1)))
            assert abs(cand.score - clamped_expected) <= 1e-5, (
                f"Candidate {cand.analysis_id} score {cand.score} != breakdown sum {clamped_expected}"
            )


def test_small_dataset_produces_fewer_than_max_selected():
    # Only 1 numeric column with 4 rows -> cannot form pairs or categorical comparisons
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})
    res = nc.explore(df, max_analyses=10)
    assert len(res.recommendations) < 10
    selected_ids = [c.analysis_id for c in res.recommendations]
    assert "numeric_relationship" not in selected_ids
    assert "categorical_numeric" not in selected_ids


def test_symmetric_redundancy_pruning():
    req = AnalysisRequirements(min_rows=3, column_kinds=(ColumnKind.NUMERIC,), min_variables=2, max_variables=2)
    c1 = AnalysisCandidate(
        analysis_id="numeric_relationship",
        analysis_type="bivariate",
        intent="Relate x and y",
        variables=("x", "y"),
        requirements=req,
        family="num_pair",
        complexity=2.0,
        score=85.0,
        status=AnalysisStatus.SELECTED,
    )
    c2 = AnalysisCandidate(
        analysis_id="numeric_relationship",
        analysis_type="bivariate",
        intent="Relate y and x",
        variables=("y", "x"),
        requirements=req,
        family="num_pair",
        complexity=2.0,
        score=80.0,
        status=AnalysisStatus.SELECTED,
    )

    reduced = apply_redundancy([c1, c2])
    rejected = [c for c in reduced if c.status == AnalysisStatus.REJECTED]
    assert len(rejected) == 1
    assert rejected[0].reject_reason == RejectReason.SYMMETRIC_DUPLICATE
