"""Requirement checks. Invalid drafts stay in the result with a machine-readable reason."""

from __future__ import annotations

from nancora.analysis.base import (
    AnalysisCandidate,
    AnalysisContext,
    CandidateDraft,
    draft_to_candidate,
)
from nancora.data.profile import DatasetProfile
from nancora.types import AnalysisStatus, RejectReason


def validate_draft(
    draft: CandidateDraft, profile: DatasetProfile, context: AnalysisContext
) -> AnalysisCandidate:
    candidate = draft_to_candidate(draft)
    req = draft.requirements
    reasons: list[str] = []
    if profile.n_rows < req.min_rows:
        reasons.append("too_few_rows")
    if len(draft.variables) < req.min_variables or len(draft.variables) > req.max_variables:
        reasons.append("variable_count")
    if req.needs_target and not context.target:
        reasons.append("missing_target")
    if context.target and req.needs_target and context.target not in draft.variables:
        reasons.append("target_not_in_variables")
    for name in draft.variables:
        col = profile.column(name)
        if col is None:
            reasons.append(f"unknown_column:{name}")
        elif req.column_kinds and col.kind not in req.column_kinds:
            reasons.append(f"invalid_kind:{name}:{col.kind.value}")
    if reasons:
        candidate.status = AnalysisStatus.INVALID
        candidate.reject_reason = RejectReason.INVALID_REQUIREMENTS
        candidate.redundancy = {"reasons": reasons}
        candidate.explanation = "Invalid: " + ", ".join(reasons)
        return candidate
    return candidate


def validate_all(
    drafts: list[CandidateDraft], profile: DatasetProfile, context: AnalysisContext
) -> list[AnalysisCandidate]:
    return [validate_draft(d, profile, context) for d in drafts]
