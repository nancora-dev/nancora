"""Numeric × numeric relationship. Reports association, never causation."""

from __future__ import annotations

import pandas as pd

from nancora.analysis.base import (
    Analysis,
    AnalysisCandidate,
    AnalysisContext,
    AnalysisRequirements,
    CandidateDraft,
    Evidence,
)
from nancora.analysis.pairing import capped_pairs, ranked_numeric_names
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.stats.tests import pearson
from nancora.types import ColumnKind


@register_analysis
class NumericRelationship(Analysis):
    id = "numeric_relationship"
    analysis_type = "bivariate"
    intent = "Measure association between two numeric columns"
    family = "numeric_pair"
    requirements = AnalysisRequirements(
        min_rows=5, column_kinds=(ColumnKind.NUMERIC,), min_variables=2, max_variables=2
    )

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        names = ranked_numeric_names(profile)
        drafts = []
        for a, b in capped_pairs(names):
            left, right = sorted((a, b))
            drafts.append(
                CandidateDraft(
                    analysis_id=self.id,
                    analysis_type=self.analysis_type,
                    intent=self.intent,
                    variables=(left, right),
                    requirements=self.requirements,
                    family=self.family,
                    complexity=2.0,
                    viz=PlotSpec(kind="scatter", title=f"{left} vs {right}", x=left, y=right),
                )
            )
        return drafts

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        a, b = candidate.variables
        stats = pearson(df[a], df[b])
        return Evidence(
            stats=dict(stats),
            provenance={
                "library": str(stats.get("library", "scipy.stats")),
                "method": str(stats.get("method", "pearson")),
            },
            notes=["Association is not causation."],
        )
