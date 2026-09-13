"""Heuristic ranking score (0–100). Not a scientifically universal quality metric."""

from __future__ import annotations

import math

from nancora.analysis.base import AnalysisCandidate, AnalysisContext, ScoreBreakdown
from nancora.data.profile import DatasetProfile

BASE_RELEVANCE = {
    "numeric_distribution": 58.0,
    "categorical_distribution": 56.0,
    "numeric_relationship": 62.0,
    "categorical_numeric": 60.0,
    "datetime_numeric_trend": 61.0,
    "correlation_analysis": 64.0,
    "outlier_analysis": 54.0,
    "missingness_analysis": 70.0,
    "cardinality_analysis": 50.0,
    "target_aware": 72.0,
}


def _finite(value, default: float = 0.0) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(v) or math.isinf(v):
        return default
    return v


def _relationship_strength(candidate: AnalysisCandidate) -> float:
    stats = candidate.evidence.stats if candidate.evidence else {}
    if "coefficient" in stats:
        return min(20.0, 20.0 * abs(_finite(stats.get("coefficient"))))
    if "strongest_abs" in stats:
        return min(18.0, 18.0 * abs(_finite(stats.get("strongest_abs"))))
    if stats.get("method") == "f_oneway":
        p = _finite(stats.get("p_value"), 1.0)
        stat = _finite(stats.get("statistic"))
        if stat <= 0:
            return 0.0
        return min(16.0, 8.0 + 8.0 * (1.0 - min(p, 1.0)))
    if "n_outliers" in stats:
        rate = _finite(stats.get("outlier_rate"))
        return min(12.0, 40.0 * rate)
    if "n_columns_with_missing" in stats:
        return min(12.0, 4.0 + 20.0 * _finite(stats.get("cell_missing_rate")))
    return 0.0


def _information_value(candidate: AnalysisCandidate, profile: DatasetProfile) -> float:
    stats = candidate.evidence.stats if candidate.evidence else {}
    n = _finite(stats.get("n"), float(profile.n_rows))
    if n <= 1:
        return -8.0
    std = stats.get("std")
    if std is not None and _finite(std) == 0:
        return -10.0
    unique_ratio = stats.get("unique_ratio")
    if unique_ratio is not None and _finite(unique_ratio) >= 0.98:
        return -4.0
    return min(8.0, math.log10(max(n, 1.0)) * 2.5)


def _data_quality(candidate: AnalysisCandidate, profile: DatasetProfile) -> float:
    missing = []
    for name in candidate.variables:
        col = profile.column(name)
        if col:
            missing.append(col.missing_rate)
    avg_missing = sum(missing) / len(missing) if missing else 0.0
    n_score = 6.0 if profile.n_rows >= 30 else 2.0 if profile.n_rows >= 8 else -4.0
    return n_score - 12.0 * avg_missing


def _complexity_penalty(candidate: AnalysisCandidate) -> float:
    return -max(0.0, (candidate.complexity - 1.0) * 2.0)


def score_candidate(
    candidate: AnalysisCandidate, profile: DatasetProfile, context: AnalysisContext
) -> AnalysisCandidate:
    if candidate.status.value == "invalid":
        candidate.score = 0.0
        candidate.breakdown = ScoreBreakdown(items=[{"name": "Invalid", "delta": 0.0}], final=0.0)
        return candidate

    base = BASE_RELEVANCE.get(candidate.analysis_id, 50.0)
    target_boost = 0.0
    if context.target and context.target in candidate.variables:
        target_boost = 14.0
    elif candidate.analysis_id == "target_aware":
        target_boost = 16.0

    rel_strength = _relationship_strength(candidate)
    info = _information_value(candidate, profile)
    quality = _data_quality(candidate, profile)
    complexity = _complexity_penalty(candidate)
    coverage = 0.0  # filled during selection

    items = [
        {
            "name": "Base relevance",
            "delta": round(base, 1),
            "signed": False,
            "note": "Heuristic prior for this analysis type",
        },
        {
            "name": "Target proximity",
            "delta": round(target_boost, 1),
            "signed": True,
            "note": "Boost if the target is involved",
        },
        {
            "name": "Relationship strength",
            "delta": round(rel_strength, 1),
            "signed": True,
            "note": "From measured association; 0 if univariate",
        },
        {
            "name": "Information value",
            "delta": round(info, 1),
            "signed": True,
            "note": "Non-degeneracy / sample support",
        },
        {
            "name": "Data quality",
            "delta": round(quality, 1),
            "signed": True,
            "note": "Sample size and missingness",
        },
        {
            "name": "Coverage",
            "delta": round(coverage, 1),
            "signed": True,
            "note": "Filled at selection time",
        },
        {
            "name": "Complexity",
            "delta": round(complexity, 1),
            "signed": True,
            "note": "Pairwise analyses cost a small penalty",
        },
    ]
    total = base + target_boost + rel_strength + info + quality + coverage + complexity
    total = max(0.0, min(100.0, total))
    total = round(total, 1)
    candidate.score = total
    candidate.breakdown = ScoreBreakdown(items=items, final=total)
    candidate.explanation = candidate.breakdown.format_trace()
    return candidate
