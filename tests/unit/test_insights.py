from nancora.analysis.evidence import insight_for
from nancora.analysis.base import AnalysisCandidate, AnalysisRequirements, Evidence


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
