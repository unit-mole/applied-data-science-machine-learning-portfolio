# Project Summary — Retrospective Election Survey Classification

| Item | Verified content |
|---|---|
| Business objective | Evaluate respondent-level party classification while explicitly separating it from representative polling or forecasting. |
| Problem type | Historical binary classification |
| Dataset | 1,525 historical survey rows with vote, age, leader ratings, economic assessments, Europe attitudes, knowledge, and gender. |
| Core methods | Stratified CV, dummy/logistic/LDA/KNN/SVM/random-forest comparison, probability calibration, untouched test evaluation, permutation importance, and age/gender sensitivity tables. |
| Final result | The calibrated random forest reaches retrospective test ROC-AUC 0.907 and balanced accuracy 0.800; this is respondent classification, not polling. |
| Decision supported | Understand classification signal and uncertainty without making live-election claims. |
| Primary evidence | `reports/figures/election_model_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

The calibrated random forest reaches retrospective test ROC-AUC 0.907 and balanced accuracy 0.800; this is respondent classification, not polling. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
