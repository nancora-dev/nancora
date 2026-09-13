"""IQR-based outlier scan for a numeric variable."""

from __future__ import annotations

import pandas as pd

from nancora.analysis.base import AnalysisContext, CandidateDraft, Evidence
from nancora.analysis.builtin._util import ranked_numeric
from nancora.analysis.evidence import evidence_from_stats
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.stats.tests import iqr_outlier_mask
from nancora.types import PlotKind


@register_analysis
class OutlierAnalysis:
    id = "outlier"
    analysis_type = "univariate"
    intent = "Flag Tukey IQR outliers in a numeric variable."

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        drafts = []
        for name in ranked_numeric(profile, context.max_univariate):
            drafts.append(
                CandidateDraft(
                    analysis_id=self.id,
                    analysis_type=self.analysis_type,
                    intent=self.intent,
                    variables=(name,),
                    requirements={"kinds": ["numeric"], "min_rows": 4},
                )
            )
        return drafts

    def compute_evidence(self, df: pd.DataFrame, draft: CandidateDraft) -> Evidence:
        name = draft.variables[0]
        stats = iqr_outlier_mask(df[name].to_numpy())
        return evidence_from_stats(
            stats,
            method="iqr",
            library="numpy",
            notes=["IQR flags are heuristic and depend on distribution shape."],
        )

    def plot_spec(self, draft: CandidateDraft, evidence: Evidence) -> PlotSpec:
        name = draft.variables[0]
        return PlotSpec(kind=PlotKind.BOX, title=f"Outliers in {name}", y=name, columns=[name])

    def insight(self, draft: CandidateDraft, evidence: Evidence) -> str:
        name = draft.variables[0]
        rate = evidence.stats.get("outlier_rate")
        n_out = evidence.stats.get("n_outliers")
        return (
            f"{name} has {n_out} IQR-flagged values (rate {rate}). "
            "Flags are heuristic, not proof of error."
        )
