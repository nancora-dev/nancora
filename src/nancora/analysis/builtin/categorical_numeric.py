"""Categorical × numeric comparison. Group association, not a causal effect."""

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
from nancora.analysis.pairing import ranked_numeric_names
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.stats.tests import f_oneway_groups
from nancora.types import CATEGORICAL_LEVEL_CAP, PAIRWISE_CAP, ColumnKind


@register_analysis
class CategoricalNumeric(Analysis):
    id = "categorical_numeric"
    analysis_type = "bivariate"
    intent = "Compare a numeric column across categorical groups"
    family = "cat_num_pair"
    requirements = AnalysisRequirements(
        min_rows=5,
        column_kinds=(ColumnKind.CATEGORICAL, ColumnKind.NUMERIC),
        min_variables=2,
        max_variables=2,
    )

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        cats = [
            n
            for n in profile.names_of(ColumnKind.CATEGORICAL, ColumnKind.BOOLEAN)
            if (profile.column(n) and profile.column(n).n_unique <= CATEGORICAL_LEVEL_CAP)
        ]
        nums = ranked_numeric_names(profile)
        drafts = []
        for cat in cats:
            for num in nums:
                drafts.append(
                    CandidateDraft(
                        analysis_id=self.id,
                        analysis_type=self.analysis_type,
                        intent=self.intent,
                        variables=(cat, num),
                        requirements=self.requirements,
                        family=self.family,
                        complexity=2.2,
                        viz=PlotSpec(kind="box", title=f"{num} by {cat}", x=cat, y=num),
                    )
                )
                if len(drafts) >= PAIRWISE_CAP:
                    return drafts
        return drafts

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        cat, num = candidate.variables
        stats = f_oneway_groups(df[num], df[cat])
        return Evidence(
            stats=dict(stats),
            provenance={
                "library": str(stats.get("library", "scipy.stats")),
                "method": str(stats.get("method", "f_oneway")),
            },
            notes=["Association is not causation."],
        )
