"""Human-readable decision traces and structured candidate explanations."""

from __future__ import annotations

from typing import Any

from nancora.analysis.base import AnalysisCandidate


def explain_decision(
    candidate: AnalysisCandidate, rejected: list[AnalysisCandidate] | None = None
) -> dict[str, Any]:
    why_not = []
    if rejected:
        cand_vars = set(candidate.variables)
        for r in rejected:
            if set(r.variables) & cand_vars or r.analysis_id == candidate.analysis_id:
                why_not.append(
                    {
                        "analysis_id": r.analysis_id,
                        "variables": list(r.variables),
                        "reason": r.reject_reason.value if r.reject_reason else r.status.value,
                        "explanation": r.explanation,
                    }
                )
    return {
        "what": {
            "analysis_id": candidate.analysis_id,
            "intent": candidate.intent,
            "variables": list(candidate.variables),
        },
        "score": candidate.score,
        "score_breakdown": candidate.breakdown.to_dict() if candidate.breakdown else None,
        "evidence": candidate.evidence.to_dict() if candidate.evidence else None,
        "why_not_others": why_not,
    }


def format_explanation(candidate: AnalysisCandidate) -> str:
    if candidate.breakdown:
        return candidate.breakdown.format_trace()
    return candidate.explanation or ""

