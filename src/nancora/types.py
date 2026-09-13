"""Shared enumerations used across schema, engine, and results."""

from __future__ import annotations

from enum import Enum


class ColumnKind(str, Enum):
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    TEXT = "text"
    UNKNOWN = "unknown"


class ColumnRole(str, Enum):
    FEATURE = "feature"
    TARGET = "target"
    ID = "id"
    CONSTANT = "constant"


class AnalysisStatus(str, Enum):
    SELECTED = "selected"
    REJECTED = "rejected"
    INVALID = "invalid"


class RejectReason(str, Enum):
    INVALID_REQUIREMENTS = "invalid_requirements"
    EXACT_DUPLICATE = "exact_duplicate"
    SYMMETRIC_DUPLICATE = "symmetric_duplicate"
    SIMILAR_ANALYSIS = "similar_analysis"
    DOMINATED = "dominated"
    COVERAGE_OVERLAP = "coverage_overlap"
    BELOW_RANK_CUTOFF = "below_rank_cutoff"


RESULT_SCHEMA_VERSION = "1"
PAIRWISE_CAP = 20
CORRELATION_COLUMN_CAP = 8
CATEGORICAL_LEVEL_CAP = 30
HIGH_CARDINALITY_UNIQUE = 50
HIGH_CARDINALITY_RATIO = 0.5
LOW_CARDINALITY_MAX = 12
