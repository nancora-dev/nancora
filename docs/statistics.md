# Statistics

`nc.stats` delegates to SciPy/Pandas:

- `pearson`, `spearman`, `kendall`
- `ks_2samp`
- `chi2_independence`
- `descriptive`
- `iqr_outlier_mask`

Every result includes `method` and `library` provenance. P-values are reported when SciPy computes them; they are not “significance theater” and do not imply causation.
