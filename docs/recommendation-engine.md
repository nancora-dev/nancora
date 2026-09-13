# Recommendation engine

`explore` and `analyze` share `run_pipeline` in `nancora.engine`.

1. Generate drafts from the registry and profile
2. Validate requirements
3. Compute evidence (lazy, per valid candidate)
4. Score with an explainable heuristic
5. Filter redundancy
6. Greedy coverage under `max_analyses`
7. Return `AnalysisResult`

`analyze` only adds a target to context; target-aware analyses then propose and receive a score boost.
