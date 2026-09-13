"""Human-readable decision traces from score breakdowns."""

from __future__ import annotations

from nancora.analysis.base import AnalysisCandidate


def format_explanation(candidate: AnalysisCandidate) -> str:
    if candidate.breakdown:
        return candidate.breakdown.format_trace()
    return candidate.explanation or ""
