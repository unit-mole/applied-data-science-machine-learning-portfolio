# Project Summary — Salary Factor Analysis and College Admissions PCA

| Item | Verified content |
|---|---|
| Business objective | Assess salary differences with robust sensitivity checks and compress correlated college indicators without hiding information loss. |
| Problem type | Factorial inference and dimensionality reduction |
| Dataset | 40 salary observations and 777 colleges with 17 numeric admissions and institutional indicators. |
| Core methods | Classic and Welch ANOVA, Kruskal sensitivity, Levene test, eta-squared, Holm-corrected pairwise Welch tests, interaction F-test, standardized PCA, loading interpretation, and reconstruction error. |
| Final result | Education shows a large observed salary association (eta²=0.626); 6 standardized components retain at least 80% of college-indicator variance. |
| Decision supported | Identify material group differences and select a defensible reduced indicator set. |
| Primary evidence | `reports/figures/anova_pca_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

Education shows a large observed salary association (eta²=0.626); 6 standardized components retain at least 80% of college-indicator variance. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
