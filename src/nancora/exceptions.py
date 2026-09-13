"""Nancora errors. Keep the surface small and actionable."""


class NancoraError(Exception):
    """Base exception for user-facing Nancora failures."""


class InputError(NancoraError):
    """Raised when input data or input types are invalid."""


class DataError(NancoraError):
    """Raised when a dataset cannot be loaded or profiled."""


class ConfigurationError(NancoraError):
    """Raised when analysis configuration parameters are invalid."""


class AnalysisError(NancoraError):
    """Raised when the recommendation pipeline cannot run."""


class ReportError(NancoraError):
    """Raised when a report cannot be written."""
