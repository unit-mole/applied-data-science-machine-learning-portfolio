# Project Summary — Holiday Package Purchase Propensity

| Item | Verified content |
|---|---|
| Business objective | Estimate purchase propensity with calibrated probabilities and expose the campaign-volume precision/recall trade-off. |
| Problem type | Binary propensity modeling |
| Dataset | 872 records with purchase outcome, salary, age, education, children, and foreign-status fields. |
| Core methods | Stratified CV, prevalence baseline, logistic/LDA/tree/forest/boosting comparison, probability calibration, training-only threshold selection, PR-AUC, ROC-AUC, customer profiling, and permutation importance. |
| Final result | Calibrated logistic regression reaches untouched-test ROC-AUC 0.730 and PR-AUC 0.707; the high-recall training threshold produces 93.0% recall with low specificity. |
| Decision supported | Choose contact thresholds consistent with capacity and false-positive/false-negative costs. |
| Primary evidence | `reports/figures/holiday_propensity_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

Calibrated logistic regression reaches untouched-test ROC-AUC 0.730 and PR-AUC 0.707; the high-recall training threshold produces 93.0% recall with low specificity. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
