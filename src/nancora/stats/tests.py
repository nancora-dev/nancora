"""SciPy/Pandas statistical delegates. Provenance is recorded by callers; we do not invent tests."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

from nancora.numeric.arrays import as_array, drop_nan


def _corr(x, y, method: str) -> dict[str, float | str]:
    xa, ya = drop_nan(as_array(x), as_array(y))
    if xa.size < 3:
        return {"n": float(xa.size), "coefficient": float("nan"), "p_value": float("nan"), "method": method}
    if method == "pearson":
        r, p = scipy_stats.pearsonr(xa, ya)
    elif method == "spearman":
        r, p = scipy_stats.spearmanr(xa, ya)
    elif method == "kendall":
        r, p = scipy_stats.kendalltau(xa, ya)
    else:
        raise ValueError(f"Unknown correlation method: {method}")
    return {
        "n": float(xa.size),
        "coefficient": float(r),
        "p_value": float(p),
        "method": method,
        "library": "scipy.stats",
    }


def pearson(x, y) -> dict[str, float | str]:
    return _corr(x, y, "pearson")


def spearman(x, y) -> dict[str, float | str]:
    return _corr(x, y, "spearman")


def kendall(x, y) -> dict[str, float | str]:
    return _corr(x, y, "kendall")


def ks_2samp(a, b) -> dict[str, float | str]:
    xa = as_array(a)
    ya = as_array(b)
    xa = xa[np.isfinite(xa)]
    ya = ya[np.isfinite(ya)]
    if xa.size < 3 or ya.size < 3:
        return {"statistic": float("nan"), "p_value": float("nan"), "method": "ks_2samp"}
    res = scipy_stats.ks_2samp(xa, ya)
    return {
        "statistic": float(res.statistic),
        "p_value": float(res.pvalue),
        "method": "ks_2samp",
        "library": "scipy.stats",
    }


def f_oneway_groups(values, groups) -> dict[str, float | str]:
    frame = pd.DataFrame({"v": pd.to_numeric(pd.Series(values), errors="coerce"), "g": pd.Series(groups)})
    frame = frame.dropna()
    samples = [g["v"].to_numpy() for _, g in frame.groupby("g") if len(g) >= 2]
    if len(samples) < 2:
        return {"statistic": float("nan"), "p_value": float("nan"), "n_groups": float(len(samples)), "method": "f_oneway"}
    stat, p = scipy_stats.f_oneway(*samples)
    return {
        "statistic": float(stat),
        "p_value": float(p),
        "n_groups": float(len(samples)),
        "method": "f_oneway",
        "library": "scipy.stats",
        "note": "Association test, not a causal claim.",
    }


def chi2_independence(a, b) -> dict[str, float | str]:
    table = pd.crosstab(pd.Series(a), pd.Series(b))
    if table.size == 0 or table.shape[0] < 2 or table.shape[1] < 2:
        return {"statistic": float("nan"), "p_value": float("nan"), "method": "chi2_contingency"}
    chi2, p, dof, _ = scipy_stats.chi2_contingency(table)
    return {
        "statistic": float(chi2),
        "p_value": float(p),
        "dof": float(dof),
        "method": "chi2_contingency",
        "library": "scipy.stats",
        "note": "Association test, not a causal claim.",
    }


def pearson_matrix(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    numeric = df[columns].apply(pd.to_numeric, errors="coerce")
    return numeric.corr(method="pearson")
