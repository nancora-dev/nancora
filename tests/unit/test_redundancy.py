from nancora.analysis.base import AnalysisCandidate, AnalysisRequirements, Evidence
from nancora.engine.redundancy import apply_redundancy
from nancora.types import AnalysisStatus


def _cand(analysis_id, variables, score, family="numeric_pair"):
    return AnalysisCandidate(
        analysis_id=analysis_id,
        analysis_type="bivariate",
        intent="t",
        variables=variables,
        requirements=AnalysisRequirements(),
        family=family,
        complexity=2.0,
        evidence=Evidence(stats={}, provenance={}),
        score=score,
        status=AnalysisStatus.SELECTED,
    )


def test_symmetric_pair_keeps_one():
    a = _cand("numeric_relationship", ("revenue", "spend"), 80)
    b = _cand("numeric_relationship", ("spend", "revenue"), 79)
    out = apply_redundancy([a, b])
    selected = [c for c in out if c.status == AnalysisStatus.SELECTED]
    rejected = [c for c in out if c.status.value == "rejected"]
    assert len(selected) == 1
    assert selected[0].variables == ("revenue", "spend")
    assert rejected[0].reject_reason.value == "symmetric_duplicate"


def test_similar_target_pair_rejected():
    a = _cand("numeric_relationship", ("x", "y"), 90, family="numeric_pair")
    b = _cand("target_aware", ("x", "y"), 70, family="target_numeric_pair")
    out = apply_redundancy([a, b])
    selected = [c for c in out if c.status == AnalysisStatus.SELECTED]
    assert len(selected) == 1
    assert selected[0].analysis_id == "numeric_relationship"
