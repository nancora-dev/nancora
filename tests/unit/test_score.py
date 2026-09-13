from nancora.analysis.base import AnalysisCandidate, AnalysisContext, Evidence
from nancora.engine.score import score_candidate


def test_strong_association_increases_score():
    weak = AnalysisCandidate(
        analysis_id="numeric_relationship",
        analysis_type="bivariate",
        intent="t",
        variables=("a", "b"),
        requirements={},
        evidence=Evidence(stats={"pearson": {"statistic": 0.05, "n": 80}}),
    )
    strong = AnalysisCandidate(
        analysis_id="numeric_relationship",
        analysis_type="bivariate",
        intent="t",
        variables=("a", "c"),
        requirements={},
        evidence=Evidence(stats={"pearson": {"statistic": 0.95, "n": 80}}),
    )
    ctx = AnalysisContext()
    weak_s = score_candidate(weak, ctx)
    strong_s = score_candidate(strong, ctx)
    assert strong_s.score > weak_s.score
    assert "Base relevance" in strong_s.breakdown.format_trace()
    assert "Final score" in strong_s.breakdown.format_trace()
