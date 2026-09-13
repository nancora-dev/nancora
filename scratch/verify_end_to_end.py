"""Manual end-to-end verification script for Nancora v0.1.0."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

import nancora as nc


def main():
    out_dir = Path("scratch/e2e_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.RandomState(42)
    n = 100

    # Dataset Type 1: Clean numeric dataset with strong linear relationship & outliers
    df1 = pd.DataFrame({
        "x": np.linspace(0, 10, n),
        "y": np.linspace(0, 20, n) + rng.randn(n) * 0.5,
        "anomalous": np.concatenate([rng.randn(95), [50.0, -40.0, 60.0, -50.0, 45.0]]),
    })

    # Dataset Type 2: High missingness dataset without outliers
    df2 = pd.DataFrame({
        "col_a": np.linspace(-1, 1, n),
        "col_b": rng.randn(n),
        "col_c": rng.choice(["A", "B", "C"], n),
    })
    df2.iloc[:40, 0] = np.nan
    df2.iloc[20:60, 1] = np.nan

    # Dataset Type 3: Customer churn dataset with boolean target
    churned = rng.rand(n) > 0.7
    df3 = pd.DataFrame({
        "churned": churned,
        "monthly_charges": np.where(churned, rng.normal(85, 10, n), rng.normal(45, 15, n)),
        "tenure_months": np.where(churned, rng.normal(6, 3, n), rng.normal(36, 12, n)),
        "plan_type": np.where(churned, rng.choice(["Basic", "Free"], n), rng.choice(["Pro", "Enterprise"], n)),
    })

    datasets = [("clean_outliers", df1, None), ("high_missing", df2, None), ("boolean_target", df3, "churned")]

    for name, df, target in datasets:
        print(f"\n==========================================")
        print(f"RUNNING MANUAL EXPLORATION: {name} (target={target})")
        print(f"==========================================")

        res = nc.explore(df, target=target)

        # 1. Inspect recommendation rankings
        print("\n--- Top 5 Recommendation Rankings ---")
        for i, rec in enumerate(res.selected[:5], 1):
            print(f"#{i} [{rec.score:.1f} pts] {rec.analysis_id} ({', '.join(rec.variables)}) - {rec.intent}")

        # 2. Verify Decision Trace
        dt = res.decision_trace
        assert "summary" in dt
        assert "selected" in dt
        assert "rejected" in dt
        print(f"Decision trace generated: {len(dt['selected'])} selected, {len(dt['rejected'])} rejected")

        # 3. Verify JSON Serialization
        json_str = res.to_json(indent=2)
        parsed = json.loads(json_str)
        assert parsed["nancora_result_version"] == "1"
        assert len(parsed["recommendations"]) == len(res.selected)
        assert len(parsed["rejected"]) == len(res.rejected)
        json_file = out_dir / f"{name}_result.json"
        json_file.write_text(json_str, encoding="utf-8")
        print(f"JSON serialization verified -> saved {json_file.name}")

        # 4. Verify HTML Report Generation
        html_file = out_dir / f"{name}_report.html"
        saved_html = res.save(html_file)
        assert saved_html.exists()
        assert saved_html.stat().st_size > 1000
        print(f"HTML report generation verified -> saved {saved_html.name} ({saved_html.stat().st_size} bytes)")

    print("\nAll end-to-end verifications passed successfully!")


if __name__ == "__main__":
    main()
