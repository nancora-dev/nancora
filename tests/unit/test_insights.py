from nancora.analysis.base import AnalysisCandidate, AnalysisRequirements, Evidence
from nancora.analysis.evidence import insight_for


def test_relationship_insight_mentions_not_causation():
    cand = AnalysisCandidate(
        analysis_id="numeric_relationship",
        analysis_type="bivariate",
        intent="rel",
        variables=("a", "b"),
        requirements=AnalysisRequirements(),
        family="numeric_pair",
        complexity=2.0,
        evidence=Evidence(stats={"coefficient": 0.9, "method": "pearson"}, provenance={}),
    )
    text = insight_for(cand).lower()
    assert "not causation" in text


def test_explain_decision():
    import nancora as nc
    from tests.conftest import mixed_frame

    res = nc.explore(mixed_frame(), max_analyses=5)
    exp = res.explain(0)
    assert "what" in exp
    assert "score" in exp
    assert "evidence" in exp
    assert "why_not_others" in exp

