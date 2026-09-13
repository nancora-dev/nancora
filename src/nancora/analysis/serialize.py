"""JSON-safe rounding for machine-readable results."""

from __future__ import annotations

from typing import Any

import numpy as np


def round_floats(value: Any, digits: int = 6) -> Any:
    if isinstance(value, dict):
        return {str(k): round_floats(v, digits) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [round_floats(v, digits) for v in value]
    if isinstance(value, (np.floating, float)):
        if np.isnan(value):
            return None
        if np.isinf(value):
            return None
        return round(float(value), digits)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, np.ndarray):
        return round_floats(value.tolist(), digits)
    return value
