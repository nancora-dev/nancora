"""Few transforms the profiler and engine actually need. Not a Pandas clone."""

from __future__ import annotations

import pandas as pd

from nancora.data.schema import infer_schema
from nancora.types import ColumnRole


def drop_constant(df: pd.DataFrame) -> pd.DataFrame:
    schema = infer_schema(df)
    keep = [c.name for c in schema if c.inferred_role != ColumnRole.CONSTANT]
    return df.loc[:, keep]


def coerce_datetime(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    out = df.copy()
    names = columns or list(out.columns)
    for name in names:
        if name not in out.columns:
            continue
        if pd.api.types.is_datetime64_any_dtype(out[name]):
            continue
        converted = pd.to_datetime(out[name], errors="coerce")
        if converted.notna().mean() >= 0.8:
            out[name] = converted
    return out
