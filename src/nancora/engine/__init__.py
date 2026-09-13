"""Explore / analyze orchestration."""

from __future__ import annotations

import time

import pandas as pd

from nancora.analysis import builtin as _builtin  # noqa: F401
from nancora.analysis.base import AnalysisCandidate, AnalysisContext
from nancora.analysis.evidence import sanitize_stats
from nancora.analysis.registry import get_analysis
from nancora.data.profile import profile as build_profile
from nancora.engine.generate import generate_candidates
from nancora.engine.rank import rank_and_select
from nancora.engine.redundancy import apply_redundancy
from nancora.engine.score import score_candidate
from nancora.engine.validate import validate_all
from nancora.exceptions import ConfigurationError, InputError
from nancora.result import AnalysisResult
from nancora.types import AnalysisStatus


def _attach_evidence(df: pd.DataFrame, candidates: list[AnalysisCandidate]) -> None:
    for cand in candidates:
        if cand.status == AnalysisStatus.INVALID:
            continue
        analysis = get_analysis(cand.analysis_id)
        evidence = analysis.compute_evidence(df, cand)
        evidence.stats = sanitize_stats(evidence.stats)
        cand.evidence = evidence
        spec = analysis.plot_spec(cand, evidence)
        if spec is not None:
            cand.viz = spec


def run_pipeline(
    df: pd.DataFrame,
    *,
    target: str | None = None,
    max_analyses: int = 10,
    rng_seed: int = 0,
) -> AnalysisResult:
    if df is None:
        raise InputError("Input dataset is None. Provide a valid pandas DataFrame.")

    if not isinstance(df, pd.DataFrame):
        raise InputError(
            f"Expected a pandas DataFrame, got {type(df).__name__}. "
            "Pass a pandas DataFrame to nancora.explore() or nancora.analyze()."
        )

    if df.empty:
        raise InputError("Cannot analyze an empty DataFrame. Provide a DataFrame containing at least one row.")

    if not isinstance(max_analyses, int) or max_analyses <= 0:
        raise ConfigurationError(
            f"max_analyses must be an integer >= 1, got {max_analyses!r}."
        )

    if df.columns.has_duplicates or not all(isinstance(c, str) for c in df.columns):
        df = df.copy()
        cols = []
        counts: dict[str, int] = {}
        for c in df.columns:
            s = str(c)
            counts[s] = counts.get(s, 0) + 1
            cols.append(s if counts[s] == 1 else f"{s}_{counts[s] - 1}")
        df.columns = pd.Index(cols)
        if target is not None and target not in df.columns and str(target) in df.columns:
            target = str(target)

    if target is not None:
        if not isinstance(target, str):
            raise InputError(
                f"Target column must be a string, got {type(target).__name__}."
            )
        if target not in df.columns:
            raise InputError(
                f"Target column not found: '{target}' in DataFrame columns {list(df.columns)}."
            )

    started = time.perf_counter()
    context = AnalysisContext(target=target, max_analyses=max_analyses, rng_seed=rng_seed)
    dset = build_profile(df, target=target)
    drafts = generate_candidates(dset, context)
    candidates = validate_all(drafts, dset, context)
    _attach_evidence(df, candidates)
    scored = [score_candidate(c, dset, context) for c in candidates]
    reduced = apply_redundancy(scored)
    selected, rejected = rank_and_select(reduced, context)
    elapsed = time.perf_counter() - started
    return AnalysisResult(
        dataset_profile=dset,
        selected=selected,
        rejected=rejected,
        context=context,
        timings={"runtime_seconds": round(elapsed, 6)},
        frame=df,
    )


def explore(
    df: pd.DataFrame,
    target: str | None = None,
    *,
    max_analyses: int = 10,
    rng_seed: int = 0,
) -> AnalysisResult:
    return run_pipeline(df, target=target, max_analyses=max_analyses, rng_seed=rng_seed)


def analyze(
    df: pd.DataFrame,
    target: str | None = None,
    *,
    max_analyses: int = 10,
    rng_seed: int = 0,
) -> AnalysisResult:
    return run_pipeline(df, target=target, max_analyses=max_analyses, rng_seed=rng_seed)
