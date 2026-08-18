# Project Summary — Insurance Claim Propensity Modeling

| Item | Verified content |
|---|---|
| Business objective | Compare and calibrate claim-propensity models using training-only selection and an untouched test set. |
| Problem type | Imbalanced binary classification |
| Dataset | 3,000 policy rows with demographic, agency, product, destination, duration, sales, commission, channel, and claim fields. |
| Core methods | Duplicate leakage control, mixed-type pipelines, dummy baseline, logistic/CART/random-forest/boosting/MLP comparison, randomized tuning, stratified CV, calibration, threshold selection, PR-AUC, and permutation importance. |
| Final result | The tuned random forest selected by training PR-AUC reaches untouched-test ROC-AUC 0.800, PR-AUC 0.618, and balanced accuracy 0.709. |
| Decision supported | Understand ranking and threshold trade-offs while keeping claim decisions under human governance. |
| Primary evidence | `reports/figures/insurance_model_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

The tuned random forest selected by training PR-AUC reaches untouched-test ROC-AUC 0.800, PR-AUC 0.618, and balanced accuracy 0.709. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
