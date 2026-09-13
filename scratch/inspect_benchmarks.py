"""Inspect benchmark recommendations and labels for ranking quality audit."""

import json
from pathlib import Path
import pandas as pd

from benchmarks.runner import run_dataset, load_labels

DATA_DIR = Path("benchmarks/datasets")

def main():
    for csv_path in sorted(DATA_DIR.glob("*.csv")):
        dataset_id = csv_path.stem
        print(f"\n==========================================")
        print(f"BENCHMARK DATASET: {dataset_id}")
        print(f"==========================================")
        labels = load_labels(dataset_id)
        print("GROUND TRUTH LABELS:")
        for lbl in labels:
            print(f"  - [{lbl['kind'].upper()}] {lbl['analysis_id']} {lbl['variables']}")
        
        rep = run_dataset(csv_path)
        print("\nMETRICS:", json.dumps(rep.get("metrics"), indent=2))
        
        df = pd.read_csv(csv_path)
        from nancora.engine import explore
        res = explore(df, max_analyses=10, rng_seed=0)
        
        print("\nTOP 10 SELECTED RECOMMENDATIONS:")
        for i, c in enumerate(res.selected[:10], 1):
            print(f"\n#{i} [{c.score:.1f} pts] {c.analysis_id} {list(c.variables)}")
            print(f"   Intent: {c.intent}")
            print(f"   Stats: {c.evidence.stats if c.evidence else {}}")
            if c.breakdown:
                deltas = [f"{item['name']}: {item['delta']:+.1f}" for item in c.breakdown.items]
                print(f"   Breakdown: {' | '.join(deltas)}")

if __name__ == "__main__":
    main()
