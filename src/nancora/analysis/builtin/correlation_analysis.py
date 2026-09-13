"""Correlation structure among numeric columns. One candidate, not a pair dump."""

from __future__ import annotations

from typing import cast

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
from nancora.stats.tests import pearson_matrix
from nancora.types import CORRELATION_COLUMN_CAP, ColumnKind


@register_analysis
class CorrelationAnalysis(Analysis):
    id = "correlation_analysis"
    analysis_type = "multivariate"
    intent = "Summarize Pearson correlations among numeric columns"
    family = "correlation_matrix"
    requirements = AnalysisRequirements(
        min_rows=5, column_kinds=(ColumnKind.NUMERIC,), min_variables=2, max_variables=32
    )

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        names = ranked_numeric_names(profile)[:CORRELATION_COLUMN_CAP]
        if len(names) < 2:
            return []
        return [
            CandidateDraft(
                analysis_id=self.id,
                analysis_type=self.analysis_type,
                intent=self.intent,
                variables=tuple(names),
                requirements=self.requirements,
                family=self.family,
                complexity=2.5,
                viz=PlotSpec(
                    kind="heatmap",
                    title="Numeric correlation matrix",
                    extra={"columns": names},
                ),
            )
        ]

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        cols = list(candidate.variables)
        matrix = pearson_matrix(df, cols)
        strongest = []
        for i, a in enumerate(cols):
            for b in cols[i + 1 :]:
                val = matrix.loc[a, b]
                if pd.notna(val):
                    fval = float(val)
                    strongest.append((abs(fval), a, b, fval))
        strongest.sort(reverse=True)
        top = strongest[0] if strongest else None
        return Evidence(
            stats={
                "n_columns": len(cols),
                "strongest_pair": [top[1], top[2]] if top else None,
                "strongest_abs": top[0] if top else None,
                "strongest_r": top[3] if top else None,
            },
            provenance={"library": "pandas", "method": "pearson_corr"},
            notes=["Correlation is not causation."],
        )
