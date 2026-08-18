# Project Summary — Statistical Methods for Decision-Making

| Item | Verified content |
|---|---|
| Business objective | Turn wholesale, student-survey, and shingle measurements into assumption-aware business and quality decisions. |
| Problem type | Statistical inference |
| Dataset | 440 wholesale customers, 62 survey respondents, and 36 shingle rows across three CSV files. |
| Core methods | Descriptive statistics, coefficients of variation, Welch tests, Mann–Whitney sensitivity, Holm correction, chi-square/Cramér's V, one-sample t and Wilcoxon tests, confidence intervals, and effect sizes. |
| Final result | Shingle B is below the 0.35 limit by both t and Wilcoxon tests (t-test p=0.0021); Shingle A is not below the limit by the prespecified t-test (p=0.075). |
| Decision supported | Prioritize category/channel investigation and decide whether moisture evidence supports a specification claim. |
| Primary evidence | `reports/figures/statistical_decision_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

Shingle B is below the 0.35 limit by both t and Wilcoxon tests (t-test p=0.0021); Shingle A is not below the limit by the prespecified t-test (p=0.075). The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
