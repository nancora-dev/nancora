import pandas as pd

from nancora.data.profile import profile
from nancora.engine.score import score_candidate
from nancora.analysis.base import AnalysisCandidate, AnalysisContext, AnalysisRequirements, Evidence
from nancora.types import AnalysisStatus


def test_score_trace_and_clamp():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, 5.0] * 6})
    prof = profile(df)
    cand = AnalysisCandidate(
        analysis_id="numeric_distribution",
        analysis_type="univariate",
        intent="dist",
        variables=("x",),
        requirements=AnalysisRequirements(),
        family="univariate_numeric",
        complexity=1.0,
        evidence=Evidence(stats={"n": 30, "mean": 3.0, "std": 1.0}, provenance={}),
        status=AnalysisStatus.SELECTED,
    )
    scored = score_candidate(cand, prof, AnalysisContext())
    assert 0 <= scored.score <= 100
    assert "Base relevance" in scored.explanation
    assert "Final score:" in scored.explanation
