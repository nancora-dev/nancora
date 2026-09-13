from pathlib import Path

from tests.conftest import mixed_frame

import nancora as nc


def test_read_csv_roundtrip(tmp_path: Path):
    path = tmp_path / "frame.csv"
    mixed_frame(n=10).to_csv(path, index=False)
    loaded = nc.read_csv(path)
    assert list(loaded.columns) == ["spend", "revenue", "noise", "region", "day", "partial"]
    assert len(loaded) == 10
