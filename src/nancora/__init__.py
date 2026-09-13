"""Nancora: recommend tabular analyses worth the user's attention."""

from __future__ import annotations

from typing import Any

import pandas as pd

from nancora import analysis as analysis
from nancora import data as data
from nancora import numeric as numpy  # curated namespace: nc.numpy
from nancora import plot as plot
from nancora import stats as stats
from nancora.analysis.registry import list_analyses, register_analysis
from nancora.data.io import read_csv, read_excel, read_json, read_parquet
from nancora.data.profile import profile
from nancora.engine import run_pipeline
from nancora.result import AnalysisResult

__version__ = "0.1.0"

__all__ = [
    "AnalysisResult",
    "analysis",
    "analyze",
    "data",
    "explore",
    "list_analyses",
    "numpy",
    "plot",
    "profile",
    "read_csv",
    "read_excel",
    "read_json",
    "read_parquet",
    "register_analysis",
    "stats",
]


def _import_builtins() -> None:
    from nancora.analysis import builtin as _builtin  # noqa: F401


_import_builtins()


def explore(
    df: pd.DataFrame,
    *,
    max_analyses: int = 10,
    rng_seed: int = 0,
) -> AnalysisResult:
    """Unsupervised analysis recommendations."""
    payload = run_pipeline(df, target=None, max_analyses=max_analyses, rng_seed=rng_seed)
    return AnalysisResult(
        _profile=payload["profile"],
        _candidates=payload["candidates"],
        _context=payload["context"],
        _timings=payload["timings"],
        _n_drafts=payload["n_drafts"],
        _df=df,
    )


def analyze(
    df: pd.DataFrame,
    target: str | None = None,
    max_analyses: int = 10,
    rng_seed: int = 0,
    **kwargs: Any,
) -> AnalysisResult:
    """Target-aware analysis recommendations. Same engine as explore()."""
    payload = run_pipeline(
        df,
        target=target,
        max_analyses=max_analyses,
        rng_seed=rng_seed,
    )
    return AnalysisResult(
        _profile=payload["profile"],
        _candidates=payload["candidates"],
        _context=payload["context"],
        _timings=payload["timings"],
        _n_drafts=payload["n_drafts"],
        _df=df,
    )
