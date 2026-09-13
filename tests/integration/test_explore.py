import json
import re

import nancora as nc
from tests.conftest import mixed_frame, target_frame


def test_explore_returns_selected_candidates(tmp_path):
    df = mixed_frame()
    path = tmp_path / "mixed.csv"
    df.to_csv(path, index=False)
    loaded = nc.read_csv(path)
    result = nc.explore(loaded)
    recs = result.recommendations()
    assert len(recs) >= 1
    payload = result.to_dict()
    assert payload["nancora_result_version"]
    json.loads(result.to_json())


def test_strong_relationship_ranks_highly():
    df = mixed_frame()
    result = nc.explore(df, max_analyses=10)
    pair_scores = [
        c.score
        for c in result.recommendations()
        if c.analysis_id == "numeric_relationship" and set(c.variables) == {"spend", "revenue"}
    ]
    noise_scores = [
        c.score
        for c in result.recommendations() + result.rejected()
        if c.analysis_id == "numeric_relationship" and set(c.variables) == {"spend", "noise"}
    ]
    assert pair_scores
    if noise_scores:
        assert pair_scores[0] >= noise_scores[0]


def test_target_analyses_prioritized():
    df = target_frame()
    result = nc.analyze(df, target="target", max_analyses=8)
    selected = result.recommendations()
    assert any(c.analysis_id == "target_aware" for c in selected)
    assert any("target" in c.variables for c in selected[:3])


def test_deterministic_json():
    df = mixed_frame()
    a = nc.explore(df, rng_seed=0).to_json()
    b = nc.explore(df, rng_seed=0).to_json()
    assert a == b


def test_insights_do_not_claim_causation():
    df = mixed_frame()
    result = nc.explore(df)
    blob = " ".join(result.insights()).lower()
    assert "causes" not in blob
    assert "caused" not in blob
    relationship = [c.insight.lower() for c in result.recommendations() if c.analysis_id == "numeric_relationship"]
    if relationship:
        assert re.search(r"association|not a causal|not causation", relationship[0])
