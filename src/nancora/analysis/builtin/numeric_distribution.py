"""Numeric distribution: what does this continuous column look like?"""

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
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.numeric.arrays import nan_aware_stats
from nancora.plot.spec import PlotSpec
from nancora.types import ColumnKind


@register_analysis
class NumericDistribution(Analysis):
    id = "numeric_distribution"
    analysis_type = "univariate"
    intent = "Describe the distribution of a numeric column"
    family = "univariate_numeric"
    requirements = AnalysisRequirements(
        min_rows=3, column_kinds=(ColumnKind.NUMERIC,), min_variables=1, max_variables=1
    )

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        drafts = []
        for name in profile.names_of(ColumnKind.NUMERIC):
            drafts.append(
                CandidateDraft(
                    analysis_id=self.id,
                    analysis_type=self.analysis_type,
                    intent=self.intent,
                    variables=(name,),
                    requirements=self.requirements,
                    family=self.family,
                    complexity=1.0,
                    viz=PlotSpec(kind="hist", title=f"Distribution of {name}", x=name),
                )
            )
        return drafts

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        name = candidate.variables[0]
        stats = nan_aware_stats(df[name])
        stats["skew"] = float(pd.to_numeric(df[name], errors="coerce").skew(skipna=True) or 0.0)
        return Evidence(
            stats=stats,
            provenance={"library": "numpy/pandas", "method": "descriptive_univariate"},
            notes=["Descriptive summary only."],
        )
