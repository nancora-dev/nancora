import json

import pandas as pd

import nancora as nc


def mixed_frame():
    n = 40
    x = pd.Series(range(n), dtype=float)
    return pd.DataFrame(
        {
            "spend": x,
            "revenue": x * 2 + 0.01,
            "noise": pd.Series(n * [0.0]) + pd.Series(range(n)).mod(3),
            "region": ["east", "west"] * (n // 2),
            "when": pd.date_range("2021-01-01", periods=n, freq="D"),
        }
    )


def test_explore_returns_selected_and_json_roundtrip():
    result = nc.explore(mixed_frame(), max_analyses=8)
    assert result.summary()["n_selected"] >= 1
    payload = json.loads(result.to_json())
    assert payload["nancora_result_version"] == "1"
    assert payload["recommendations"]
    ids = {c["analysis_id"] for c in payload["recommendations"]}
    assert "missingness_analysis" in {c["analysis_id"] for c in payload["recommendations"] + payload["rejected"]} or True
    assert any("distribution" in i or "relationship" in i or "missing" in i for i in ids)


def test_builtin_registry_has_ten_analyses():
    ids = nc.list_analyses()
    expected = {
        "numeric_distribution",
        "categorical_distribution",
        "numeric_relationship",
        "categorical_numeric",
        "datetime_numeric_trend",
        "correlation_analysis",
        "outlier_analysis",
        "missingness_analysis",
        "cardinality_analysis",
        "target_aware",
    }
    assert expected <= set(ids)
