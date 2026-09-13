"""Candidate generation from the registry and dataset profile."""

from __future__ import annotations

from nancora.analysis.base import AnalysisContext, CandidateDraft
from nancora.analysis.registry import all_analyses
from nancora.data.profile import DatasetProfile


def generate_candidates(profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
    drafts: list[CandidateDraft] = []
    for analysis in all_analyses():
        if analysis.requirements.needs_target and not context.target:
            continue
        drafts.extend(analysis.propose(profile, context))
    drafts.sort(key=lambda d: (d.analysis_id, d.variables))
    return drafts
