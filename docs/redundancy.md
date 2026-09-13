# Redundancy

Rules:

- exact duplicates (same analysis id and variables)
- symmetric duplicates (`Revenue × Spend` vs `Spend × Revenue`)
- similar analyses (same family and variables, e.g. distribution vs outlier on one column)
- dominated analyses (variable subset of a stronger family member)
- coverage overlap for competing univariate views

Reasons: `exact_duplicate`, `symmetric_duplicate`, `similar_analysis`, `dominated`, `coverage_overlap`, `below_rank_cutoff`, `invalid_requirements`.
