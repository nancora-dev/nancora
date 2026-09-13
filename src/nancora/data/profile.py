"""Dataset profiling. Cheap dataset-level evidence for candidate generation — not a full EDA dump."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from nancora.data.schema import ColumnSchema, infer_schema, is_high_cardinality
from nancora.types import ColumnKind, ColumnRole


@dataclass
class DatasetProfile:
    n_rows: int
    n_cols: int
    columns: list[ColumnSchema]
    kind_counts: dict[str, int]
    high_cardinality: list[str] = field(default_factory=list)
    top_missing: list[tuple[str, float]] = field(default_factory=list)
    target: str | None = None

    @property
    def n_columns(self) -> int:
        return self.n_cols

    @property
    def missing_columns(self) -> list[str]:
        return [name for name, _ in self.top_missing]


    def column(self, name: str) -> ColumnSchema | None:
        for col in self.columns:
            if col.name == name:
                return col
        return None

    def names_of(self, *kinds: ColumnKind, include_id: bool = False) -> list[str]:
        out: list[str] = []
        for col in self.columns:
            if col.kind not in kinds:
                continue
            if not include_id and col.inferred_role == ColumnRole.ID:
                continue
            if col.inferred_role == ColumnRole.CONSTANT:
                continue
            out.append(col.name)
        return out

    def to_dict(self) -> dict:
        return {
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "columns": [c.to_dict() for c in self.columns],
            "kind_counts": dict(self.kind_counts),
            "high_cardinality": list(self.high_cardinality),
            "top_missing": [{"name": n, "missing_rate": r} for n, r in self.top_missing],
            "target": self.target,
        }


def profile(df: pd.DataFrame, *, target: str | None = None) -> DatasetProfile:
    columns = infer_schema(df)
    if target is not None:
        columns = [
            ColumnSchema(
                name=c.name,
                kind=c.kind,
                n_unique=c.n_unique,
                missing_rate=c.missing_rate,
                inferred_role=ColumnRole.TARGET if c.name == target else c.inferred_role,
                n_non_null=c.n_non_null,
                variance=c.variance,
            )
            for c in columns
        ]
    kind_counts: dict[str, int] = {}
    for col in columns:
        kind_counts[col.kind.value] = kind_counts.get(col.kind.value, 0) + 1
    n_rows = int(len(df))
    high = [c.name for c in columns if is_high_cardinality(c, n_rows)]
    missing = sorted(
        ((c.name, c.missing_rate) for c in columns if c.missing_rate > 0),
        key=lambda x: x[1],
        reverse=True,
    )[:10]
    return DatasetProfile(
        n_rows=n_rows,
        n_cols=int(df.shape[1]),
        columns=columns,
        kind_counts=kind_counts,
        high_cardinality=high,
        top_missing=missing,
        target=target,
    )
