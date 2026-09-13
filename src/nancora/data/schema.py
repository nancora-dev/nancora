"""Column schema inference. Delegates typing to pandas dtypes plus cardinality heuristics."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd

from nancora.types import (
    HIGH_CARDINALITY_RATIO,
    HIGH_CARDINALITY_UNIQUE,
    LOW_CARDINALITY_MAX,
    ColumnKind,
    ColumnRole,
)


@dataclass(frozen=True)
class ColumnSchema:
    name: str
    kind: ColumnKind
    n_unique: int
    missing_rate: float
    inferred_role: ColumnRole
    n_non_null: int
    variance: float | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["kind"] = self.kind.value
        d["inferred_role"] = self.inferred_role.value
        return d


def infer_column_kind(series: pd.Series, n_unique: int, n_non_null: int) -> ColumnKind:
    if n_non_null == 0:
        return ColumnKind.UNKNOWN
    if pd.api.types.is_bool_dtype(series):
        return ColumnKind.BOOLEAN
    if pd.api.types.is_datetime64_any_dtype(series):
        return ColumnKind.DATETIME
    if pd.api.types.is_numeric_dtype(series):
        if n_unique <= 2:
            return ColumnKind.BOOLEAN if set(series.dropna().unique()) <= {0, 1, True, False} else ColumnKind.CATEGORICAL
        if n_unique <= LOW_CARDINALITY_MAX and n_unique / max(n_non_null, 1) < 0.05:
            return ColumnKind.CATEGORICAL
        return ColumnKind.NUMERIC
    if isinstance(series.dtype, pd.CategoricalDtype):
        return ColumnKind.CATEGORICAL
    if pd.api.types.is_string_dtype(series) or series.dtype == object:
        sample = series.dropna().astype(str)
        if n_unique <= LOW_CARDINALITY_MAX * 2:
            return ColumnKind.CATEGORICAL
        avg_len = float(sample.str.len().mean()) if len(sample) else 0.0
        if avg_len > 40:
            return ColumnKind.TEXT
        return ColumnKind.CATEGORICAL if n_unique <= 50 else ColumnKind.TEXT
    return ColumnKind.UNKNOWN


def infer_role(name: str, kind: ColumnKind, n_unique: int, n_rows: int) -> ColumnRole:
    lowered = name.strip().lower()
    if n_unique <= 1:
        return ColumnRole.CONSTANT
    id_tokens = ("id", "uuid", "guid", "pk", "index")
    if lowered in id_tokens or lowered.endswith("_id") or lowered.endswith("id"):
        if n_unique >= max(10, int(0.9 * n_rows)):
            return ColumnRole.ID
    if n_unique == n_rows and n_rows > 5 and kind in {ColumnKind.NUMERIC, ColumnKind.TEXT, ColumnKind.CATEGORICAL}:
        return ColumnRole.ID
    return ColumnRole.FEATURE


def infer_schema(df: pd.DataFrame) -> list[ColumnSchema]:
    n_rows = len(df)
    columns: list[ColumnSchema] = []
    for name in df.columns:
        series = df[name]
        n_non_null = int(series.notna().sum())
        n_unique = int(series.nunique(dropna=True))
        missing_rate = 1.0 - (n_non_null / n_rows) if n_rows else 1.0
        kind = infer_column_kind(series, n_unique, n_non_null)
        role = infer_role(str(name), kind, n_unique, n_rows)
        variance = None
        if kind == ColumnKind.NUMERIC and n_non_null > 1:
            variance = float(pd.to_numeric(series, errors="coerce").var(skipna=True) or 0.0)
        columns.append(
            ColumnSchema(
                name=str(name),
                kind=kind,
                n_unique=n_unique,
                missing_rate=float(missing_rate),
                inferred_role=role,
                n_non_null=n_non_null,
                variance=variance,
            )
        )
    return columns


def is_high_cardinality(col: ColumnSchema, n_rows: int) -> bool:
    if n_rows <= 0:
        return False
    ratio = col.n_unique / n_rows
    return col.n_unique > HIGH_CARDINALITY_UNIQUE and ratio > HIGH_CARDINALITY_RATIO
