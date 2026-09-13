"""Missingness overview across the frame."""

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


@register_analysis
class MissingnessAnalysis(Analysis):
    id = "missingness_analysis"
    analysis_type = "dataset"
    intent = "Summarize missing values across columns"
    family = "data_quality"
    requirements = AnalysisRequirements(min_rows=1, min_variables=1, max_variables=10_000)

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        names = tuple(c.name for c in profile.columns)
        if not names:
            return []
        return [
            CandidateDraft(
                analysis_id=self.id,
                analysis_type=self.analysis_type,
                intent=self.intent,
                variables=names[:20],
                requirements=self.requirements,
                family=self.family,
                complexity=1.1,
                viz=PlotSpec(
                    kind="bar",
                    title="Missingness (top columns shown in report tables)",
                    x=names[0],
                ),
            )
        ]

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        rates = {str(c): float(df[c].isna().mean()) for c in df.columns}
        n_missing_cols = sum(1 for v in rates.values() if v > 0)
        return Evidence(
            stats={
                "n_columns_with_missing": n_missing_cols,
                "cell_missing_rate": float(df.isna().mean().mean()) if len(df.columns) else 0.0,
                "worst_column": max(rates, key=lambda k: rates[k]) if rates else None,
                "worst_rate": max(rates.values()) if rates else 0.0,
            },
            provenance={"library": "pandas", "method": "isna.mean"},
            notes=["Missingness is a data-quality observation, not an imputation."],
        )
