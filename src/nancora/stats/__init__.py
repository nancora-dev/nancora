"""Curated statistics (SciPy-backed) consumed by builtin analyses."""

from nancora.stats.tests import (
    chi2_independence,
    f_oneway_groups,
    kendall,
    ks_2samp,
    pearson,
    pearson_matrix,
    spearman,
)

__all__ = [
    "chi2_independence",
    "f_oneway_groups",
    "kendall",
    "ks_2samp",
    "pearson",
    "pearson_matrix",
    "spearman",
]
