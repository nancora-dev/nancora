"""Shared synthetic frames for tests."""

from __future__ import annotations

import numpy as np
import pandas as pd


def mixed_frame(n: int = 80, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    spend = rng.normal(100, 15, n)
    revenue = 2.0 * spend + rng.normal(0, 3, n)
    noise = rng.normal(0, 20, n)
    region = rng.choice(["north", "south", "east"], n)
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    missing = spend.copy()
    missing[:8] = np.nan
    return pd.DataFrame(
        {
            "spend": spend,
            "revenue": revenue,
            "noise": noise,
            "region": region,
            "day": dates,
            "partial": missing,
        }
    )


def target_frame(n: int = 60, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, n)
    target = 1.5 * x + rng.normal(0, 0.2, n)
    cat = np.where(target > 0, "high", "low")
    return pd.DataFrame({"feature": x, "other": rng.normal(0, 1, n), "target": target, "band": cat})
