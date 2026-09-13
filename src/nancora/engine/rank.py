"""Rank and select with a greedy coverage bonus under max_analyses."""

from __future__ import annotations

from nancora.analysis.base import AnalysisCandidate, AnalysisContext
from nancora.types import AnalysisStatus, RejectReason


def rank_and_select(
    candidates: list[AnalysisCandidate], context: AnalysisContext
) -> tuple[list[AnalysisCandidate], list[AnalysisCandidate]]:
    pool = [c for c in candidates if c.status == AnalysisStatus.SELECTED]
    others = [c for c in candidates if c.status != AnalysisStatus.SELECTED]
    pool.sort(key=lambda c: (-(c.score or 0.0), c.analysis_id, c.variables))

    selected: list[AnalysisCandidate] = []
    covered: set[tuple[str, str]] = set()
    for cand in pool:
        if len(selected) >= context.max_analyses:
            cand.status = AnalysisStatus.REJECTED
            cand.reject_reason = RejectReason.BELOW_RANK_CUTOFF
            cand.redundancy = {"reason": RejectReason.BELOW_RANK_CUTOFF.value}
            others.append(cand)
            continue
        new_units = {(v, cand.analysis_id) for v in cand.variables} - covered
        bonus = min(8.0, 2.0 * len(new_units)) if new_units else -1.0
        cand.coverage = round(bonus, 1)
        if cand.breakdown:
            for item in cand.breakdown.items:
                if item["name"] == "Coverage":
                    item["delta"] = cand.coverage
            total = min(100.0, max(0.0, (cand.score or 0.0) + cand.coverage))
            cand.score = round(total, 1)
            cand.breakdown.final = cand.score
            cand.explanation = cand.breakdown.format_trace()
        selected.append(cand)
        covered |= {(v, cand.analysis_id) for v in cand.variables}

    selected.sort(key=lambda c: (-(c.score or 0.0), c.analysis_id, c.variables))
    others.sort(key=lambda c: (c.status.value, -(c.score or 0.0), c.analysis_id, c.variables))
    return selected, others
