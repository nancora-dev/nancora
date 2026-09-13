from nancora.analysis.base import AnalysisCandidate, Evidence, ScoreBreakdown
from nancora.engine.redundancy import apply_redundancy
from nancora.types import AnalysisStatus, RejectReason


def _cand(analysis_id: str, variables: tuple[str, ...], score: float) -> AnalysisCandidate:
    return AnalysisCandidate(
        analysis_id=analysis_id,
        analysis_type="bivariate" if len(variables) == 2 else "univariate",
        intent="test",
        variables=variables,
        requirements={},
        evidence=Evidence(),
        score=score,
        breakdown=ScoreBreakdown(items=[{"name": "Base relevance", "delta": score, "base": True}], final=score),
        status=AnalysisStatus.SELECTED,
    )


def test_symmetric_duplicates_keep_one():
    left = _cand("numeric_relationship", ("revenue", "spend"), 90.0)
    right = _cand("numeric_relationship", ("spend", "revenue"), 88.0)
    out = apply_redundancy([left, right])
    selected = [c for c in out if c.status != AnalysisStatus.REJECTED]
    rejected = [c for c in out if c.status == AnalysisStatus.REJECTED]
    assert len(selected) == 1
    assert selected[0].variables == ("revenue", "spend")
    assert rejected[0].reject_reason == RejectReason.SYMMETRIC_DUPLICATE


def test_similar_family_keeps_higher_score():
    dist = _cand("numeric_distribution", ("spend",), 70.0)
    dist.analysis_type = "univariate"
    outlier = _cand("outlier", ("spend",), 80.0)
    outlier.analysis_type = "univariate"
    out = apply_redundancy([dist, outlier])
    rejected = [c for c in out if c.status == AnalysisStatus.REJECTED]
    kept = [c for c in out if c.status != AnalysisStatus.REJECTED]
    assert len(kept) == 1
    assert kept[0].analysis_id == "outlier"
    assert rejected[0].reject_reason == RejectReason.SIMILAR_ANALYSIS
