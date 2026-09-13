"""Basic Unsupervised Exploration Example with Nancora."""

import pandas as pd
import nancora as nc


def main():
    # 1. Create a sample dataset
    df = pd.DataFrame({
        "age": [22, 25, 47, 52, 46, 56, 48, 33, 27, 29],
        "income": [25000, 32000, 75000, 89000, 71000, 95000, 82000, 49000, 39000, 42000],
        "city": ["Surat", "Surat", "Mumbai", "Delhi", "Mumbai", "Delhi", "Surat", "Mumbai", "Delhi", "Surat"],
        "purchased": ["no", "no", "yes", "yes", "yes", "yes", "yes", "no", "no", "no"],
    })

    print(f"Dataset Loaded: {len(df)} rows, {len(df.columns)} columns")

    # 2. Run unsupervised exploration
    result = nc.explore(df)

    # 3. Print high-level summary
    summary = result.summary()
    print(f"\nRecommendations Selected: {summary['n_selected']}")
    print(f"Analyses Skipped/Redundant: {summary['n_rejected']}")

    # 4. Display top recommendations
    print("\n--- Top Recommendations ---")
    for rec in result.recommendations[:3]:
        print(f"[{rec.score:.1f}] {rec.analysis_id} on {rec.variables}: {rec.intent}")

    # 5. Display key natural language insights
    print("\n--- Key Insights ---")
    for insight in result.insights:
        print(f"• {insight}")


if __name__ == "__main__":
    main()
