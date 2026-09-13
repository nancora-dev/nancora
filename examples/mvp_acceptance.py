"""Nancora Final MVP Acceptance Test Script

Demonstrates end-to-end unsupervised and target-aware exploration workflow:
DATASET -> PROFILING -> CANDIDATE GENERATION -> APPLICABILITY -> EVIDENCE
        -> SCORING -> REDUNDANCY -> RANKING -> EXPLANATION -> VISUALIZATION -> REPORT
"""

from pathlib import Path
import pandas as pd
import nancora as nc


def main():
    print("==================================================================")
    print("          NANCORA FINAL MVP ACCEPTANCE TEST RUNNER                ")
    print("==================================================================")

    # 1. Prepare sample dataset
    df = pd.DataFrame(
        {
            "tenure_months": [1, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66],
            "monthly_charges": [29.9, 45.5, 65.0, 70.2, 85.0, 89.9, 95.5, 99.0, 102.5, 105.0, 110.0, 115.0],
            "total_charges": [29.9, 273.0, 780.0, 1263.6, 2040.0, 2697.0, 3438.0, 4158.0, 4920.0, 5670.0, 6600.0, 7590.0],
            "contract_type": ["month-to-month", "month-to-month", "one-year", "one-year", "two-year", "two-year",
                              "month-to-month", "one-year", "two-year", "two-year", "two-year", "two-year"],
            "churned": ["yes", "yes", "no", "no", "no", "no", "yes", "no", "no", "no", "no", "no"],
        }
    )

    print("\n[1] DATASET LOADED:")
    print(f"    Rows: {len(df)}, Columns: {list(df.columns)}")

    # 2. Unsupervised Exploration
    print("\n[2] RUNNING UNSUPERVISED EXPLORATION (nc.explore(df)):")
    res_unsupervised = nc.explore(df)

    print(f"    Profile: {res_unsupervised.profile.n_rows} rows, {res_unsupervised.profile.n_cols} cols")
    print(f"    Recommendations Selected: {len(res_unsupervised.recommendations)}")
    print(f"    Analyses Skipped / Redundant: {len(res_unsupervised.rejected_candidates)}")

    print("\n    TOP RECOMMENDATIONS:")
    for i, rec in enumerate(res_unsupervised.recommendations[:3], 1):
        print(f"      #{i} Score: {rec.score:.1f} | ID: {rec.analysis_id} | Vars: {rec.variables}")
        print(f"         Intent: {rec.intent}")

    print("\n    KEY INSIGHTS:")
    for insight in res_unsupervised.insights[:3]:
        print(f"      - {insight}")

    # 3. Target-Aware Exploration
    print("\n[3] RUNNING TARGET-AWARE EXPLORATION (nc.explore(df, target='churned')):")
    res_target = nc.explore(df, target="churned")

    print(f"    Target Column: '{res_target.context.target}'")
    print(f"    Recommendations Selected: {len(res_target.recommendations)}")

    print("\n    TOP TARGET-AWARE RECOMMENDATIONS:")
    for i, rec in enumerate(res_target.recommendations[:3], 1):
        print(f"      #{i} Score: {rec.score:.1f} | ID: {rec.analysis_id} | Vars: {rec.variables}")
        print(f"         Explanation: {rec.explanation}")

    # 4. Decision Trace & Explanations
    print("\n[4] DECISION TRACE & INTENTIONAL SKIPS:")
    trace = res_target.decision_trace
    print(f"    Total Selected in Trace: {len(trace['selected'])}")
    print(f"    Total Rejected in Trace: {len(trace['rejected'])}")
    if trace['rejected']:
        sample_rej = trace['rejected'][0]
        print(f"    Sample Rejection: {sample_rej['analysis_id']} ({sample_rej['variables']}) -> Reason: {sample_rej['reason']}")

    # 5. Visualizations & HTML Report Saving
    print("\n[5] VISUALIZATIONS & REPORT GENERATION:")
    figs = res_target.visualizations
    print(f"    Rendered Matplotlib Figures: {len(figs)}")

    out_file = Path("mvp_acceptance_report.html")
    res_target.save(out_file)
    print(f"    HTML Report Saved to: {out_file.resolve()} (Size: {out_file.stat().st_size} bytes)")

    print("\n==================================================================")
    print("       NANCORA FINAL MVP ACCEPTANCE TEST COMPLETED SUCCESSFULLY    ")
    print("==================================================================")


if __name__ == "__main__":
    main()
