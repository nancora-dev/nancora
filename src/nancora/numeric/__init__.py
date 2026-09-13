"""Curated numeric helpers (NumPy-backed) consumed by builtin analyses."""

from nancora.numeric.arrays import as_array, drop_nan, iqr_outlier_mask, nan_aware_stats

__all__ = ["as_array", "drop_nan", "iqr_outlier_mask", "nan_aware_stats"]
