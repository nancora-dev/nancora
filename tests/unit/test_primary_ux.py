import json
from pathlib import Path
import pandas as pd
import nancora as nc
from nancora.result import ExplorationResult, CallableList

def sample_df():
    return pd.DataFrame({
        "age": [25, 30, 35, 40, 45, 50, 55, 60],
        "income": [50000, 60000, 75000, 90000, 110000, 125000, 140000, 160000],
        "churn": ["no", "no", "yes", "no", "yes", "yes", "no", "yes"],
    })

def test_explore_api_and_exploration_result_alias():
    df = sample_df()
    result = nc.explore(df)
    assert isinstance(result, ExplorationResult)

def test_target_aware_explore():
    df = sample_df()
    result = nc.explore(df, target="churn")
    assert result.context.target == "churn"
    # Target-aware candidate should be present
    selected_ids = [c.analysis_id for c in result.recommendations]
    assert "target_aware" in selected_ids

def test_exploration_result_properties():
    df = sample_df()
    result = nc.explore(df)

    # profile
    assert result.profile.n_rows == 8
    assert result.profile.n_cols == 3

    # recommendations (CallableList)
    assert isinstance(result.recommendations, list)
    assert isinstance(result.recommendations, CallableList)
    assert result.recommendations() == result.recommendations

    # insights
    assert len(result.insights) == len(result.recommendations)
    assert result.insights() == result.insights

    # rejected_candidates
    assert isinstance(result.rejected_candidates, list)
    assert result.rejected_candidates() == result.rejected_candidates

    # visualizations
    viz_list = result.visualizations
    assert isinstance(viz_list, list)

    # decision_trace
    trace = result.decision_trace
    assert "summary" in trace
    assert "selected" in trace
    assert "rejected" in trace

def test_serialization_methods(tmp_path: Path):
    df = sample_df()
    result = nc.explore(df, target="churn")

    d = result.to_dict()
    assert d["nancora_result_version"] == "1"
    assert "profile" in d
    assert "recommendations" in d
    assert "rejected" in d
    assert "context" in d

    js = result.to_json()
    parsed = json.loads(js)
    assert parsed["context"]["target"] == "churn"

    # save html
    html_path = tmp_path / "report.html"
    saved = result.save(html_path)
    assert saved.exists()
    assert "Nancora" in html_path.read_text(encoding="utf-8")

def test_notebook_repr_html():
    df = sample_df()
    result = nc.explore(df, target="churn")
    html = result._repr_html_()

    assert "Nancora Exploration Result" in html
    assert "Recommendations" in html
    assert "Prioritized Recommendations" in html
    assert "Key Analytical Insights" in html
    assert "churn" in html
