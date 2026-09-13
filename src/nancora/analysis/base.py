"""Core analysis abstractions: drafts, evidence, candidates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.types import AnalysisStatus, ColumnKind, RejectReason


@dataclass(frozen=True)
class AnalysisContext:
    target: str | None = None
    max_analyses: int = 10
    rng_seed: int = 0


@dataclass
class AnalysisRequirements:
    min_rows: int = 3
    column_kinds: tuple[ColumnKind, ...] = ()
    min_variables: int = 1
    max_variables: int = 2
    needs_target: bool = False

    def to_dict(self) -> dict:
        return {
            "min_rows": self.min_rows,
            "column_kinds": [k.value for k in self.column_kinds],
            "min_variables": self.min_variables,
            "max_variables": self.max_variables,
            "needs_target": self.needs_target,
        }


@dataclass
class Evidence:
    stats: dict[str, Any]
    provenance: dict[str, str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "stats": dict(self.stats),
            "provenance": dict(self.provenance),
            "notes": list(self.notes),
        }


@dataclass
class ScoreBreakdown:
    items: list[dict[str, Any]]
    final: float

    def format_trace(self) -> str:
        lines = [
            f"{row['name']}: {row['delta']:+.1f}"
            if row.get("signed")
            else f"{row['name']}: {row['delta']:.1f}"
            for row in self.items
        ]
        lines.append(f"Final score: {self.final:.1f}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {"items": list(self.items), "final": self.final, "trace": self.format_trace()}


@dataclass
class CandidateDraft:
    analysis_id: str
    analysis_type: str
    intent: str
    variables: tuple[str, ...]
    requirements: AnalysisRequirements
    family: str
    complexity: float
    viz: PlotSpec | None = None


@dataclass
class AnalysisCandidate:
    analysis_id: str
    analysis_type: str
    intent: str
    variables: tuple[str, ...]
    requirements: AnalysisRequirements
    family: str
    complexity: float
    evidence: Evidence | None = None
    score: float | None = None
    coverage: float = 0.0
    redundancy: dict[str, Any] = field(default_factory=dict)
    status: AnalysisStatus = AnalysisStatus.SELECTED
    reject_reason: RejectReason | None = None
    explanation: str = ""
    breakdown: ScoreBreakdown | None = None
    viz: PlotSpec | None = None

    def canonical_vars(self) -> tuple[str, ...]:
        return tuple(sorted(self.variables))

    def to_dict(self) -> dict:
        return {
            "analysis_id": self.analysis_id,
            "analysis_type": self.analysis_type,
            "intent": self.intent,
            "variables": list(self.variables),
            "requirements": self.requirements.to_dict(),
            "family": self.family,
            "complexity": self.complexity,
            "evidence": self.evidence.to_dict() if self.evidence else None,
            "score": self.score,
            "coverage": self.coverage,
            "redundancy": dict(self.redundancy),
            "status": self.status.value,
            "reject_reason": self.reject_reason.value if self.reject_reason else None,
            "explanation": self.explanation,
            "breakdown": self.breakdown.to_dict() if self.breakdown else None,
            "viz": self.viz.to_dict() if self.viz else None,
        }


def draft_to_candidate(
    draft: CandidateDraft, status: AnalysisStatus = AnalysisStatus.SELECTED
) -> AnalysisCandidate:
    return AnalysisCandidate(
        analysis_id=draft.analysis_id,
        analysis_type=draft.analysis_type,
        intent=draft.intent,
        variables=draft.variables,
        requirements=draft.requirements,
        family=draft.family,
        complexity=draft.complexity,
        status=status,
        viz=draft.viz,
    )


class Analysis(ABC):
    id: str
    analysis_type: str
    intent: str
    family: str
    requirements: AnalysisRequirements

    @abstractmethod
    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        raise NotImplementedError

    @abstractmethod
    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        raise NotImplementedError

    def plot_spec(self, candidate: AnalysisCandidate, evidence: Evidence) -> PlotSpec | None:
        return candidate.viz
