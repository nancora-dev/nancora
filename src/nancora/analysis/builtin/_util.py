"""Shared proposal helpers. Pairwise generation is capped."""

from __future__ import annotations

from itertools import combinations

import numpy as np
import pandas as pd

from nancora.data.profile import DatasetProfile
from nancora.types import ColumnKind, ColumnRole, MAX_PAIRS, MAX_UNIVARIATE, PAIRWISE_SAMPLE_ROWS


def ranked_numeric(profile: DatasetProfile, limit: int = MAX_UNIVARIATE) -> list[str]:
    cols = [
        c
        for c in profile.columns
        if c.kind == ColumnKind.NUMERIC and c.inferred_role not in {ColumnRole.ID, ColumnRole.CONSTANT}
    ]
    cols.sort(key=lambda c: (c.missing_rate, -c.n_unique, c.name))
    return [c.name for c in cols[:limit]]


def ranked_categorical(profile: DatasetProfile, limit: int = MAX_UNIVARIATE) -> list[str]:
    cols = [
        c
        for c in profile.columns
        if c.kind in {ColumnKind.CATEGORICAL, ColumnKind.BOOLEAN}
        and c.inferred_role not in {ColumnRole.ID, ColumnRole.CONSTANT}
        and 2 <= c.n_unique <= 50
    ]
    cols.sort(key=lambda c: (c.n_unique > 20, c.missing_rate, c.name))
    return [c.name for c in cols[:limit]]


def ranked_datetime(profile: DatasetProfile, limit: int = MAX_UNIVARIATE) -> list[str]:
    cols = [
        c
        for c in profile.columns
        if c.kind == ColumnKind.DATETIME and c.inferred_role != ColumnRole.CONSTANT
    ]
    cols.sort(key=lambda c: (c.missing_rate, c.name))
    return [c.name for c in cols[:limit]]


def cheap_abs_corr(df: pd.DataFrame, a: str, b: str) -> float:
    sample = df[[a, b]].dropna()
    if len(sample) > PAIRWISE_SAMPLE_ROWS:
        sample = sample.iloc[:PAIRWISE_SAMPLE_ROWS]
    if len(sample) < 3:
        return 0.0
    x = sample[a].to_numpy(dtype=float)
    y = sample[b].to_numpy(dtype=float)
    if np.std(x) == 0 or np.std(y) == 0:
        return 0.0
    value = np.corrcoef(x, y)[0, 1]
    if np.isnan(value):
        return 0.0
    return float(abs(value))


def top_numeric_pairs(
    df: pd.DataFrame,
    names: list[str],
    limit: int = MAX_PAIRS,
) -> list[tuple[str, str, float]]:
    scored: list[tuple[str, str, float]] = []
    for a, b in combinations(sorted(names), 2):
        scored.append((a, b, cheap_abs_corr(df, a, b)))
    scored.sort(key=lambda item: (-item[2], item[0], item[1]))
    return scored[:limit]
