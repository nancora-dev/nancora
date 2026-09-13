"""Missingness overview for the table."""

from __future__ import annotations

import pandas as pd

from nancora.analysis.base import AnalysisContext, CandidateDraft, Evidence
from nancora.analysis.evidence import evidence_from_stats
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.types import PlotKind


@register_analysis
class MissingnessAnalysis:
    id = "missingness"
    analysis_type = "quality"
    intent = "Quantify missing values across columns."

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        names = tuple(col.name for col in profile.columns)
        if not names:
            return []
        return [
            CandidateDraft(
                analysis_id=self.id,
                analysis_type=self.analysis_type,
                intent=self.intent,
                variables=names,
                requirements={"min_rows": 1},
            )
        ]

    def compute_evidence(self, df: pd.DataFrame, draft: CandidateDraft) -> Evidence:
        rates = {col: float(df[col].isna().mean()) for col in df.columns}
        stats = {
            "missing_rates": rates,
            "n_columns_with_missing": int(sum(1 for v in rates.values() if v > 0)),
            "any_missing": bool(any(v > 0 for v in rates.values())),
        }
        return evidence_from_stats(stats, method="isna_mean", library="pandas")

    def plot_spec(self, draft: CandidateDraft, evidence: Evidence) -> PlotSpec:
        return PlotSpec(
            kind=PlotKind.MISSING,
            title="Missingness by column",
            columns=list(draft.variables),
        )

    def insight(self, draft: CandidateDraft, evidence: Evidence) -> str:
        n = evidence.stats.get("n_columns_with_missing")
        if not evidence.stats.get("any_missing"):
            return "No missing values were detected in this table."
        return f"{n} columns contain missing values."
