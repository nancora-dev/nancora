"""Datetime × numeric trend (descriptive)."""

from __future__ import annotations

import pandas as pd

from nancora.analysis.base import AnalysisContext, CandidateDraft, Evidence
from nancora.analysis.builtin._util import ranked_datetime, ranked_numeric
from nancora.analysis.evidence import evidence_from_stats
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.stats.tests import pearson
from nancora.types import PlotKind


@register_analysis
class DatetimeNumericTrend:
    id = "datetime_numeric"
    analysis_type = "bivariate"
    intent = "Describe how a numeric variable changes over a datetime index."

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        dts = ranked_datetime(profile, 4)
        nums = ranked_numeric(profile, 8)
        drafts = []
        for dt in dts:
            for num in nums:
                drafts.append(
                    CandidateDraft(
                        analysis_id=self.id,
                        analysis_type=self.analysis_type,
                        intent=self.intent,
                        variables=(dt, num),
                        requirements={"kinds": ["datetime", "numeric"], "min_rows": 3},
                    )
                )
        drafts.sort(key=lambda d: d.variables)
        return drafts[: context.max_pairs]

    def compute_evidence(self, df: pd.DataFrame, draft: CandidateDraft) -> Evidence:
        dt, num = draft.variables
        times = pd.to_datetime(df[dt], errors="coerce")
        if int(times.notna().sum()) < 3:
            stats = {
                "n": int(times.notna().sum()),
                "start": None,
                "end": None,
                "time_association": {
                    "method": "pearson",
                    "library": "scipy.stats.pearsonr",
                    "n": 0,
                    "statistic": float("nan"),
                    "pvalue": float("nan"),
                },
            }
        else:
            delta = (times - times.min()).dt.total_seconds()
            assoc = pearson(delta.to_numpy(dtype=float), df[num].to_numpy())
            stats = {
                "n": int(times.notna().sum()),
                "start": str(times.min()),
                "end": str(times.max()),
                "time_association": assoc,
            }
        return evidence_from_stats(
            stats,
            method="time_ordinal_pearson",
            library="pandas+scipy.stats.pearsonr",
            notes=["Time association is descriptive and is not a causal trend claim."],
        )

    def plot_spec(self, draft: CandidateDraft, evidence: Evidence) -> PlotSpec:
        dt, num = draft.variables
        return PlotSpec(
            kind=PlotKind.LINE,
            title=f"{num} over {dt}",
            x=dt,
            y=num,
            columns=[dt, num],
        )

    def insight(self, draft: CandidateDraft, evidence: Evidence) -> str:
        dt, num = draft.variables
        return (
            f"{num} is plotted against {dt} from {evidence.stats.get('start')} "
            f"to {evidence.stats.get('end')}. Association with time is not causation."
        )
