# Analysis registry

Builtin IDs:

1. numeric_distribution
2. categorical_distribution
3. numeric_relationship
4. categorical_numeric
5. datetime_numeric_trend
6. correlation_analysis
7. outlier_analysis
8. missingness_analysis
9. cardinality_analysis
10. target_aware

Register more with `@nc.register_analysis` on a class implementing `propose`, `compute_evidence`, and `plot_spec`. There is no plugin marketplace in the MVP.
