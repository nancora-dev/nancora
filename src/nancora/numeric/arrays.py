"""NumPy helpers used by analyses. This is not a NumPy API clone."""

from __future__ import annotations

import numpy as np
import pandas as pd


def as_array(values, *, dtype=float) -> np.ndarray:
    series = pd.to_numeric(pd.Series(values), errors="coerce")
    arr = np.asarray(series, dtype=dtype)
    return arr


def drop_nan(*arrays: np.ndarray) -> tuple[np.ndarray, ...]:
    mask = np.ones(len(arrays[0]), dtype=bool)
    for arr in arrays:
        mask &= np.isfinite(arr)
    return tuple(arr[mask] for arr in arrays)


def nan_aware_stats(values) -> dict[str, float]:
    arr = as_array(values)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {
            "n": 0.0,
            "mean": float("nan"),
            "std": float("nan"),
            "min": float("nan"),
            "max": float("nan"),
            "median": float("nan"),
        }
    return {
        "n": float(finite.size),
        "mean": float(np.mean(finite)),
        "std": float(np.std(finite, ddof=1)) if finite.size > 1 else 0.0,
        "min": float(np.min(finite)),
        "max": float(np.max(finite)),
        "median": float(np.median(finite)),
    }


def iqr_outlier_mask(values) -> np.ndarray:
    arr = as_array(values)
    finite = np.isfinite(arr)
    out = np.zeros(arr.shape, dtype=bool)
    data = arr[finite]
    if data.size < 4:
        return out
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    if iqr == 0:
        return out
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    out[finite] = (data < lo) | (data > hi)
    return out
