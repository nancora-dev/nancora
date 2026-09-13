"""IQR outlier screen. A heuristic fence, not a contamination model."""

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
from nancora.numeric.arrays import iqr_outlier_mask, nan_aware_stats
from nancora.plot.spec import PlotSpec
from nancora.types import ColumnKind


@register_analysis
class OutlierAnalysis(Analysis):
    id = "outlier_analysis"
    analysis_type = "univariate"
    intent = "Flag IQR outliers on a numeric column"
    family = "univariate_numeric"
    requirements = AnalysisRequirements(
        min_rows=8, column_kinds=(ColumnKind.NUMERIC,), min_variables=1, max_variables=1
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
                    family="outlier_numeric",
                    complexity=1.4,
                    viz=PlotSpec(kind="hist", title=f"Outlier screen: {name}", x=name),
                )
            )
        return drafts

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        name = candidate.variables[0]
        mask = iqr_outlier_mask(df[name])
        stats = nan_aware_stats(df[name])
        stats["n_outliers"] = int(mask.sum())
        stats["outlier_rate"] = float(mask.mean()) if mask.size else 0.0
        return Evidence(
            stats=stats,
            provenance={"library": "numpy", "method": "iqr_1.5"},
            notes=["IQR fences are a heuristic, not a generative outlier model."],
        )
