"""Evidence helpers: rounding and insight templates. Never fabricate coefficients."""

from __future__ import annotations

from math import isfinite

from nancora.analysis.base import AnalysisCandidate


def round_number(value, digits: int = 6):
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if not isfinite(value):
            return None
        return round(value, digits)
    return value


def sanitize_stats(stats: dict) -> dict:
    out = {}
    for key, val in stats.items():
        if isinstance(val, dict):
            out[key] = sanitize_stats(val)
        elif isinstance(val, list):
            out[key] = [round_number(v) if isinstance(v, (int, float)) else v for v in val]
        else:
            out[key] = round_number(val) if isinstance(val, (int, float)) else val
    return out


def insight_for(candidate: AnalysisCandidate) -> str:
    ev = candidate.evidence
    stats = ev.stats if ev else {}
    vars_ = ", ".join(candidate.variables)
    aid = candidate.analysis_id
    if aid == "numeric_distribution":
        return (
            f"{vars_} is numeric (n={stats.get('n')}, mean={stats.get('mean')}, "
            f"median={stats.get('median')}). This is a distribution summary, not a causal finding."
        )
    if aid == "categorical_distribution":
        return f"{vars_} is categorical with {stats.get('n_levels')} observed levels (top={stats.get('top_level')})."
    if aid == "numeric_relationship":
        r = stats.get("coefficient")
        return (
            f"Association between {vars_}: {stats.get('method')} coefficient={r}. "
            "Association is not causation."
        )
    if aid == "categorical_numeric":
        return (
            f"Group comparison of {candidate.variables[-1] if candidate.variables else vars_} "
            f"across {candidate.variables[0] if candidate.variables else 'groups'} "
            f"({stats.get('method')} statistic={stats.get('statistic')}). Association is not causation."
        )
    if aid == "datetime_numeric_trend":
        return (
            f"Time trend of {candidate.variables[1] if len(candidate.variables) > 1 else vars_} "
            f"versus {candidate.variables[0] if candidate.variables else 'time'} "
            f"(ordinal association={stats.get('coefficient')}). Association is not causation."
        )
    if aid == "correlation_analysis":
        return (
            f"Pearson correlation structure among {len(candidate.variables)} numeric columns. "
            "Correlation is not causation."
        )
    if aid == "outlier_analysis":
        return f"IQR outlier screen on {vars_}: {stats.get('n_outliers')} flagged points (heuristic fence, not a model)."
    if aid == "missingness_analysis":
        return f"Missingness overview: {stats.get('n_columns_with_missing')} columns have missing values."
    if aid == "cardinality_analysis":
        return f"Cardinality of {vars_}: {stats.get('n_unique')} unique values (ratio={stats.get('unique_ratio')})."
    if aid == "target_aware":
        return (
            f"Target-aware view for {vars_}. Ranking favors target-linked questions; "
            "this is not a predictive model."
        )
    return f"{candidate.intent} ({vars_})."


def evidence_notes(*notes: str) -> list[str]:
    return [n for n in notes if n]
