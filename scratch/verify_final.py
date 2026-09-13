"""Final verification script for all Nancora user-facing APIs and determinism."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

import nancora as nc


def main():
    rng = np.random.RandomState(42)
    n = 100
    df = pd.DataFrame({
        "churned": rng.rand(n) > 0.7,
        "spend": rng.normal(50, 10, n),
        "income": rng.normal(60000, 15000, n),
        "region": rng.choice(["North", "South", "East"], n),
    })

    # 1. nc.explore(df)
    res1 = nc.explore(df, rng_seed=42)
    assert len(res1.selected) > 0

    # 2. nc.explore(df, target="churned")
    res2 = nc.explore(df, target="churned", rng_seed=42)
    assert len(res2.selected) > 0
    assert res2.selected[0].analysis_id == "target_aware"

    # 3. result.explain()
    exp0 = res2.explain(0)
    assert "score_breakdown" in exp0 or "selected_candidate" in exp0

    # 4. result.to_dict()
    d = res2.to_dict()
    assert d["nancora_result_version"] == "1"

    # 5. result.to_json()
    j = res2.to_json()
    assert len(j) > 100

    # 6. result.save("report.html")
    p = res2.save("scratch/test_report.html")
    assert p.exists()

    # 7. Jupyter representation (_repr_html_)
    html_repr = res2._repr_html_()
    assert "<table" in html_repr
    assert "Nancora Exploration Result" in html_repr

    # 8. Deterministic repeated runs
    run_a = nc.explore(df, target="churned", rng_seed=123).to_dict()
    run_b = nc.explore(df, target="churned", rng_seed=123).to_dict()
    del run_a['timings']
    del run_b['timings']
    del run_a['summary']['runtime_seconds']
    del run_b['summary']['runtime_seconds']
    assert run_a == run_b, "Repeated runs with same seed must produce identical recommendations and scores"

    print("All final API, determinism, and representation checks PASSED!")


if __name__ == "__main__":
    main()
