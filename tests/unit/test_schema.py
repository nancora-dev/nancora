from pathlib import Path

import pandas as pd

from nancora.data.io import read_csv
from nancora.data.profile import profile
from nancora.data.schema import infer_schema
from nancora.types import ColumnKind


def test_read_csv_and_kinds(tmp_path: Path):
    path = tmp_path / "tiny.csv"
    path.write_text("n,cat,flag\n1,a,1\n2,b,0\n3,a,1\n", encoding="utf-8")
    df = read_csv(path)
    schema = infer_schema(df)
    kinds = {c.name: c.kind for c in schema}
    assert kinds["n"] == ColumnKind.NUMERIC
    assert kinds["cat"] == ColumnKind.CATEGORICAL
    prof = profile(df)
    assert prof.n_rows == 3
    assert prof.n_cols == 3


def test_datetime_and_missing():
    df = pd.DataFrame(
        {
            "when": pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"]),
            "y": [1.0, None, 3.0],
        }
    )
    prof = profile(df)
    kinds = {c.name: c.kind for c in prof.columns}
    assert kinds["when"] == ColumnKind.DATETIME
    assert prof.top_missing[0][0] == "y"
