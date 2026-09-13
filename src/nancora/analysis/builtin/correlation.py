"""Focused correlation matrix for numeric columns. Association, not causation."""

from __future__ import annotations

import pandas as pd

from nancora.analysis.base import AnalysisContext, CandidateDraft, Evidence
from nancora.analysis.builtin._util import ranked_numeric
from nancora.analysis.evidence import evidence_from_stats
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.types import PlotKind


@register_analysis
class CorrelationAnalysis:
    id = "correlation"
    analysis_type = "multivariate"
    intent = "Summarize pairwise Pearson associations among numeric variables."

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        names = ranked_numeric(profile, limit=12)
        if len(names) < 2:
            return []
        return [
            CandidateDraft(
                analysis_id=self.id,
                analysis_type=self.analysis_type,
                intent=self.intent,
                variables=tuple(names),
                requirements={"kinds": ["numeric"], "min_rows": 3, "min_vars": 2},
            )
        ]

    def compute_evidence(self, df: pd.DataFrame, draft: CandidateDraft) -> Evidence:
        cols = list(draft.variables)
        corr = df[cols].corr(method="pearson")
        matrix = {
            str(r): {str(c): (None if pd.isna(corr.loc[r, c]) else float(corr.loc[r, c])) for c in corr.columns}
            for r in corr.index
        }
        stats = {"method": "pearson", "matrix": matrix, "n_columns": len(cols)}
        return evidence_from_stats(
            stats,
            method="pearson_matrix",
            library="pandas.DataFrame.corr",
            notes=["Correlation is an association measure, not a causal finding."],
        )

    def plot_spec(self, draft: CandidateDraft, evidence: Evidence) -> PlotSpec:
        return PlotSpec(
            kind=PlotKind.HEATMAP,
            title="Pearson correlation matrix",
            columns=list(draft.variables),
        )

    def insight(self, draft: CandidateDraft, evidence: Evidence) -> str:
        n = evidence.stats.get("n_columns")
        return (
            f"Pearson correlation matrix over {n} numeric columns. "
            "Associations are not causal."
        )
