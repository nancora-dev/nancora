import json
import re

import numpy as np
import pandas as pd

import nancora as nc
from nancora.analysis.base import AnalysisCandidate, AnalysisRequirements, Evidence
from nancora.engine.redundancy import apply_redundancy
from nancora.types import AnalysisStatus


def strong_vs_noise(n: int = 80) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    x = rng.normal(size=n)
    return pd.DataFrame(
        {
            "x": x,
            "y": x * 3 + rng.normal(scale=0.05, size=n),
            "noise": rng.normal(size=n),
            "group": rng.choice(["a", "b"], size=n),
        }
    )


def test_strong_relationship_ranks_highly():
    result = nc.explore(strong_vs_noise(), max_analyses=10)
    pair_scores = {}
    for cand in result.selected + result.rejected:
        if cand.analysis_id == "numeric_relationship" and cand.score is not None:
            pair_scores[tuple(sorted(cand.variables))] = cand.score
    assert pair_scores[("x", "y")] > pair_scores[("noise", "x")]
    assert pair_scores[("x", "y")] > pair_scores[("noise", "y")]


def test_target_prioritized():
    df = strong_vs_noise()
    result = nc.analyze(df, target="y", max_analyses=8)
    selected_ids = [c.analysis_id for c in result.recommendations()]
    assert "target_aware" in selected_ids
    target_scores = [c.score for c in result.recommendations() if c.analysis_id == "target_aware"]
    assert target_scores
    assert max(target_scores) >= min(c.score or 0 for c in result.recommendations())


def test_deterministic_json():
    df = strong_vs_noise()
    a = json.loads(nc.explore(df, max_analyses=6, rng_seed=0).to_json())
    b = json.loads(nc.explore(df, max_analyses=6, rng_seed=0).to_json())
    a["timings"] = {}
    b["timings"] = {}
    a["summary"]["runtime_seconds"] = None
    b["summary"]["runtime_seconds"] = None
    assert a == b


def test_insights_avoid_causal_claims():
    result = nc.explore(strong_vs_noise(), max_analyses=8)
    blob = " ".join(result.insights()).lower()
    assert "causation" in blob
    assert not re.search(r"\bcauses\b", blob)


def test_symmetric_in_engine_unit_path():
    req = AnalysisRequirements()
    ev = Evidence(stats={"coefficient": 0.9}, provenance={})
    a = AnalysisCandidate(
        analysis_id="numeric_relationship",
        analysis_type="bivariate",
        intent="rel",
        variables=("revenue", "spend"),
        requirements=req,
        family="numeric_pair",
        complexity=2.0,
        evidence=ev,
        score=88.0,
        status=AnalysisStatus.SELECTED,
    )
    b = AnalysisCandidate(
        analysis_id="numeric_relationship",
        analysis_type="bivariate",
        intent="rel",
        variables=("spend", "revenue"),
        requirements=req,
        family="numeric_pair",
        complexity=2.0,
        evidence=ev,
        score=87.0,
        status=AnalysisStatus.SELECTED,
    )
    out = apply_redundancy([a, b])
    selected = [c for c in out if c.status == AnalysisStatus.SELECTED]
    assert len(selected) == 1
