# Retrospective Election Survey Classification

> **Value proposition:** Evaluate respondent-level party classification while explicitly separating it from representative polling or forecasting.

![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg) ![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg) ![Notebook](https://img.shields.io/badge/Notebook-Executed-F37626.svg)

## Executive summary

**Business question.** Evaluate respondent-level party classification while explicitly separating it from representative polling or forecasting.  
**Dataset.** 1,525 historical survey rows with vote, age, leader ratings, economic assessments, Europe attitudes, knowledge, and gender.  
**Verified result.** The calibrated random forest reaches retrospective test ROC-AUC 0.907 and balanced accuracy 0.800; this is respondent classification, not polling.  
**Decision value.** Understand classification signal and uncertainty without making live-election claims.  
**Primary limitation.** The undocumented sampling and weighting design prevents representative election inference or future-election claims.

![Primary evidence](reports/figures/election_model_evidence.png)

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<https://github.com/unit-mole/Election_Exit_Poll_Prediction_using_ML_Models>)

## Business problem

The intended user is **A survey-methodology analyst**. The analysis supports this decision: **Understand classification signal and uncertainty without making live-election claims.** It does not claim causality or production readiness unless the study design supports that claim.

## Analytical questions and success criteria

1. What data-quality issues materially affect the analysis?
2. Which baseline establishes the minimum useful performance or descriptive reference?
3. Which method is selected under a leakage-safe validation design?
4. How stable, calibrated, or assumption-sensitive is the result?
5. What action is supported, and what action remains outside scope?

Technical success requires a fully executed pipeline, correct split logic, task-appropriate metrics, saved evidence, deterministic seeds where supported, and zero notebook errors. Business success requires an interpretable result that changes a defensible analytical decision without fabricating financial impact.

## Dataset and provenance

1,525 historical survey rows with vote, age, leader ratings, economic assessments, Europe attitudes, knowledge, and gender.

Bundled in the original repository; survey organization, weighting, sampling design, and license are undocumented.

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

## Methodology

Stratified CV, dummy/logistic/LDA/KNN/SVM/random-forest comparison, probability calibration, untouched test evaluation, permutation importance, and age/gender sensitivity tables.

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

## Validation strategy

```json
{
  "training_rows": 1143,
  "untouched_test_rows": 382,
  "selection": "5-fold stratified CV on training only",
  "selection_metric": "ROC-AUC",
  "random_seed": 42
}
```

## Verified result

> The calibrated random forest reaches retrospective test ROC-AUC 0.907 and balanced accuracy 0.800; this is respondent classification, not polling.

### Primary comparison table

| model | cv_roc_auc_mean | cv_roc_auc_std | cv_balanced_accuracy_mean | cv_f1_mean |
|---|---|---|---|---|
| random_forest | 0.882 | 0.026 | 0.803 | 0.863 |
| linear_discriminant_analysis | 0.881 | 0.017 | 0.783 | 0.879 |
| support_vector_machine | 0.880 | 0.029 | 0.814 | 0.860 |
| logistic_regression | 0.879 | 0.017 | 0.808 | 0.855 |
| knn | 0.872 | 0.028 | 0.776 | 0.877 |
| dummy_majority | 0.500 | 0.000 | 0.500 | 0.822 |

All values above are generated from the committed data and synchronized with `reports/metrics.json` after execution.

## Explainability, diagnostics, and robustness

- The project saves its comparison and diagnostic tables under `reports/tables/`.
- The primary figure combines model/statistical evidence with error, stability, calibration, or profile evidence appropriate to the task.
- Predictive projects compare against a baseline and preserve an untouched holdout.
- Statistical projects report assumptions, effect size, and robust alternatives.
- Clustering projects report internal metrics as descriptive evidence—not proof of objectively real groups.
- Time-series projects use chronological origins and transparent baselines.

## Business recommendations

| Priority | Recommendation | Evidence | Expected benefit | Risk or limitation | How to measure success |
|---:|---|---|---|---|---|
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | The calibrated random forest reaches retrospective test ROC-AUC 0.907 and balanced accuracy 0.800; this is respondent classification, not polling. | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
| 2 | Review the largest error, uncertainty, or sensitivity segment before deployment. | See saved diagnostic tables | Reduces hidden failure risk | Small subgroups can produce unstable estimates | Track subgroup error and interval coverage |
| 3 | Keep a transparent baseline in future monitoring. | Baseline comparison is recorded in the notebook | Detects when complexity stops adding value | Baselines do not capture every business driver | Compare every refresh against the same baseline |

## Limitations and responsible use

See the executed metrics for project-specific limitations.

The undocumented sampling and weighting design prevents representative election inference or future-election claims.

## Repository structure

```text
07-election-exit-poll-prediction/
├── data/README.md
├── notebooks/01_end_to_end_analysis.ipynb
├── src/analysis.py
├── reports/figures/
├── reports/tables/
├── reports/metrics.json
├── models/                 # when a fitted artifact is useful
├── PROJECT_SUMMARY.md
└── README.md
```

## Run locally

From the portfolio root:

```bash
python projects/07-election-exit-poll-prediction/src/analysis.py
python scripts/execute_notebooks.py --project 07-election-exit-poll-prediction
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/07-election-exit-poll-prediction/reports/` and, for selected predictive models, `projects/07-election-exit-poll-prediction/models/`.

## Technologies and skills demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Historical binary classification · reproducibility · responsible interpretation.

## Future work

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

## Interview-ready explanation

“I rebuilt this as a historical binary classification case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.”

## Résumé bullets

- Re-engineered a political survey research analysis into a reproducible historical binary classification workflow with automated data-quality evidence, saved outputs, and a fully executed recruiter-facing notebook.
- Implemented stratified cv and problem-appropriate validation to produce the verified result: The calibrated random forest reaches retrospective test ROC-AUC 0.907 and balanced accuracy 0.800; this is respondent classification, not polling.
- Translated model/statistical diagnostics into prioritized recommendations while documenting provenance, uncertainty, and responsible-use limits.
