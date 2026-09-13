"""Target-Aware Exploration Example with Nancora."""

import pandas as pd
import nancora as nc


def main():
    # 1. Create a customer churn dataset
    df = pd.DataFrame({
        "tenure_months": [1, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66],
        "monthly_charges": [29.9, 45.5, 65.0, 70.2, 85.0, 89.9, 95.5, 99.0, 102.5, 105.0, 110.0, 115.0],
        "contract_type": ["month-to-month", "month-to-month", "one-year", "one-year", "two-year", "two-year",
                          "month-to-month", "one-year", "two-year", "two-year", "two-year", "two-year"],
        "churn": ["yes", "yes", "no", "no", "no", "no", "yes", "no", "no", "no", "no", "no"],
    })

    print(f"Customer Churn Dataset: {len(df)} rows")

    # 2. Run target-aware exploration focused on "churn"
    result = nc.analyze(df, target="churn")

    print(f"\nTarget Variable: '{result.context.target}'")
    print(f"Top Recommendations Selected: {len(result.recommendations)}")

    # 3. Print target-focused recommendations
    print("\n--- Top Target Recommendations ---")
    for rec in result.recommendations[:3]:
        print(f"[{rec.score:.1f}] {rec.analysis_id} ({', '.join(rec.variables)})")

    # 4. Save self-contained HTML report
    report_path = "churn_target_report.html"
    result.save(report_path)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
