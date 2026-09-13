"""Pair-generation helpers that cap combinatorial explosion."""

from __future__ import annotations

from itertools import combinations

from nancora.data.profile import DatasetProfile
from nancora.types import PAIRWISE_CAP, ColumnKind, ColumnRole


def ranked_numeric_names(profile: DatasetProfile, exclude: set[str] | None = None) -> list[str]:
    exclude = exclude or set()
    cols = [
        c
        for c in profile.columns
        if c.kind == ColumnKind.NUMERIC
        and c.inferred_role != ColumnRole.CONSTANT
        and c.name not in exclude
        and (c.inferred_role != ColumnRole.ID)
    ]
    cols.sort(key=lambda c: (c.variance is None, -(c.variance or 0.0), c.name))
    return [c.name for c in cols]


def capped_pairs(names: list[str], cap: int = PAIRWISE_CAP) -> list[tuple[str, str]]:
    pairs = [(a, b) for a, b in combinations(names, 2)]
    pairs.sort(key=lambda p: (p[0], p[1]))
    return pairs[:cap]
