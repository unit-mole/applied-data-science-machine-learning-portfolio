# Project Summary — Online Retail Customer Segmentation

| Item | Verified content |
|---|---|
| Business objective | Create auditable customer profiles after explicit cancellation, return, duplicate, and missing-ID treatment. |
| Problem type | Unsupervised RFM segmentation |
| Dataset | 541,909 UCI Online Retail transaction rows from December 2010 through December 2011. |
| Core methods | Transaction cleaning, customer-level RFM, log scaling, K-means/Gaussian-mixture comparison, silhouette/Davies–Bouldin/Calinski–Harabasz metrics, seed stability, outlier sensitivity, PCA, and evidence-based naming. |
| Final result | The pipeline segments 4,338 customers into 2 stable RFM groups (silhouette 0.432, seed ARI 0.999). |
| Decision supported | Design differentiated retention and reactivation experiments without sensitive profiling. |
| Primary evidence | `reports/figures/online_retail_segmentation_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

The pipeline segments 4,338 customers into 2 stable RFM groups (silhouette 0.432, seed ARI 0.999). The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
