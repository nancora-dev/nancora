"""File Loading and Report Generation Example with Nancora."""

from pathlib import Path
import pandas as pd
import nancora as nc


def main():
    # 1. Save temporary sample CSV file
    sample_path = Path("sample_data.csv")
    df_sample = pd.DataFrame({
        "score_a": [88, 92, 75, 64, 99, 85, 90],
        "score_b": [85, 90, 78, 62, 95, 88, 92],
        "passed": [True, True, True, False, True, True, True],
    })
    df_sample.to_csv(sample_path, index=False)

    # 2. Load CSV using Nancora IO helper
    df = nc.read_csv(sample_path)
    print(f"Loaded '{sample_path}': {len(df)} rows, {list(df.columns)}")

    # 3. Explore dataset
    result = nc.explore(df)

    # 4. Serialize to JSON string
    json_output = result.to_json(indent=2)
    print("\n--- JSON Result Preview (first 250 chars) ---")
    print(json_output[:250] + "...")

    # Cleanup sample CSV file
    if sample_path.exists():
        sample_path.unlink()


if __name__ == "__main__":
    main()
