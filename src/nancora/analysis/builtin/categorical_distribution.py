"""Categorical distribution: which levels appear, and how often?"""

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
from nancora.plot.spec import PlotSpec
from nancora.types import CATEGORICAL_LEVEL_CAP, ColumnKind


@register_analysis
class CategoricalDistribution(Analysis):
    id = "categorical_distribution"
    analysis_type = "univariate"
    intent = "Describe the distribution of a categorical column"
    family = "univariate_categorical"
    requirements = AnalysisRequirements(
        min_rows=3,
        column_kinds=(ColumnKind.CATEGORICAL, ColumnKind.BOOLEAN),
        min_variables=1,
        max_variables=1,
    )

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        drafts = []
        for name in profile.names_of(ColumnKind.CATEGORICAL, ColumnKind.BOOLEAN):
            col = profile.column(name)
            if col and col.n_unique > CATEGORICAL_LEVEL_CAP:
                continue
            drafts.append(
                CandidateDraft(
                    analysis_id=self.id,
                    analysis_type=self.analysis_type,
                    intent=self.intent,
                    variables=(name,),
                    requirements=self.requirements,
                    family=self.family,
                    complexity=1.0,
                    viz=PlotSpec(kind="bar", title=f"Counts of {name}", x=name),
                )
            )
        return drafts

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        name = candidate.variables[0]
        counts = df[name].astype("string").value_counts(dropna=True).head(20)
        top = str(counts.index[0]) if len(counts) else None
        return Evidence(
            stats={
                "n_levels": int(df[name].nunique(dropna=True)),
                "top_level": top,
                "top_count": int(counts.iloc[0]) if len(counts) else 0,
                "n": int(df[name].notna().sum()),
            },
            provenance={"library": "pandas", "method": "value_counts"},
            notes=["Level frequencies only."],
        )
