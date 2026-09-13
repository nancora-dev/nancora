import json

import nancora as nc
from tests.conftest import mixed_frame


def test_regression_json_stable_keys(tmp_path):
    result = nc.explore(mixed_frame(), max_analyses=5)
    payload = json.loads(result.to_json())
    assert set(payload) >= {
        "nancora_result_version",
        "summary",
        "profile",
        "recommendations",
        "rejected",
        "insights",
        "context",
    }
    for rec in payload["recommendations"]:
        assert "score" in rec
        assert "explanation" in rec
        assert rec["breakdown"] is not None
    for rec in payload["rejected"]:
        assert rec["reject_reason"] is not None or rec["status"] == "invalid"
