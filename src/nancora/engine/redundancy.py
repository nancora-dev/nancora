"""Redundancy filtering: exact, symmetric, similar, dominated, coverage overlap."""

from __future__ import annotations

from nancora.analysis.base import AnalysisCandidate
from nancora.types import AnalysisStatus, RejectReason

SIMILAR_FAMILIES = {
    frozenset({"numeric_pair", "target_numeric_pair"}),
    frozenset({"cat_num_pair", "target_cat_num"}),
    frozenset({"univariate_numeric", "outlier_numeric"}),
}


def _pair_key(variables: tuple[str, ...]) -> tuple[str, ...]:
    if len(variables) == 2:
        return tuple(sorted(variables))
    return variables


def apply_redundancy(candidates: list[AnalysisCandidate]) -> list[AnalysisCandidate]:
    valid = [c for c in candidates if c.status != AnalysisStatus.INVALID]
    invalid = [c for c in candidates if c.status == AnalysisStatus.INVALID]

    seen_exact: dict[tuple, AnalysisCandidate] = {}
    for cand in valid:
        key = (cand.analysis_id, cand.canonical_vars())
        prev = seen_exact.get(key)
        if prev is None:
            seen_exact[key] = cand
            continue
        loser, winner = (cand, prev) if (cand.score or 0) <= (prev.score or 0) else (prev, cand)
        _reject(loser, RejectReason.EXACT_DUPLICATE, winner)
        seen_exact[key] = winner

    remaining = list(seen_exact.values())

    seen_sym: dict[tuple, AnalysisCandidate] = {}
    survivors: list[AnalysisCandidate] = []
    for cand in remaining:
        if cand.status == AnalysisStatus.REJECTED:
            survivors.append(cand)
            continue
        key = (cand.analysis_id, _pair_key(cand.variables))
        prev = seen_sym.get(key)
        if prev is None:
            seen_sym[key] = cand
            survivors.append(cand)
            continue
        if cand.variables != prev.variables:
            loser, winner = (cand, prev) if (cand.score or 0) <= (prev.score or 0) else (prev, cand)
            _reject(loser, RejectReason.SYMMETRIC_DUPLICATE, winner)
            if winner is cand:
                seen_sym[key] = cand
            survivors.append(cand)
        else:
            survivors.append(cand)

    active = [c for c in survivors if c.status == AnalysisStatus.SELECTED]
    active.sort(key=lambda c: (-(c.score or 0), c.analysis_id, c.variables))

    for i, cand in enumerate(active):
        for other in active[:i]:
            if cand.status != AnalysisStatus.SELECTED:
                break
            if _similar(cand, other):
                _reject(cand, RejectReason.SIMILAR_ANALYSIS, other)
            elif _dominated(cand, other):
                _reject(cand, RejectReason.DOMINATED, other)
            elif _coverage_overlap(cand, other):
                _reject(cand, RejectReason.COVERAGE_OVERLAP, other)

    return invalid + survivors


def _similar(a: AnalysisCandidate, b: AnalysisCandidate) -> bool:
    if a.analysis_id == b.analysis_id:
        return False
    fam = frozenset({a.family, b.family})
    if fam not in SIMILAR_FAMILIES:
        return False
    if len(a.variables) == 2 and len(b.variables) == 2:
        return _pair_key(a.variables) == _pair_key(b.variables)
    if len(a.variables) == 1 and len(b.variables) == 1:
        return a.variables == b.variables
    return False


def _dominated(a: AnalysisCandidate, b: AnalysisCandidate) -> bool:
    if a.analysis_id != b.analysis_id:
        return False
    aset, bset = set(a.variables), set(b.variables)
    return aset < bset and (a.score or 0) <= (b.score or 0)


def _coverage_overlap(a: AnalysisCandidate, b: AnalysisCandidate) -> bool:
    if a.analysis_id != b.analysis_id:
        return False
    if a.analysis_id in {"numeric_distribution", "categorical_distribution", "cardinality_analysis", "outlier_analysis"}:
        return a.variables == b.variables
    return False


def _reject(loser: AnalysisCandidate, reason: RejectReason, winner: AnalysisCandidate) -> None:
    loser.status = AnalysisStatus.REJECTED
    loser.reject_reason = reason
    loser.redundancy = {
        "reason": reason.value,
        "kept": {"analysis_id": winner.analysis_id, "variables": list(winner.variables)},
    }
    extra = f"Rejected ({reason.value}); kept {winner.analysis_id} {list(winner.variables)}"
    loser.explanation = (loser.explanation + "\n" + extra).strip()
