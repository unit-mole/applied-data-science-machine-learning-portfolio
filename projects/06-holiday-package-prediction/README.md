# Holiday Package Purchase Propensity

> **Value proposition:** Estimate purchase propensity with calibrated probabilities and expose the campaign-volume precision/recall trade-off.

![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg) ![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg) ![Notebook](https://img.shields.io/badge/Notebook-Executed-F37626.svg)

## Executive summary

**Business question.** Estimate purchase propensity with calibrated probabilities and expose the campaign-volume precision/recall trade-off.  
**Dataset.** 872 records with purchase outcome, salary, age, education, children, and foreign-status fields.  
**Verified result.** Calibrated logistic regression reaches untouched-test ROC-AUC 0.730 and PR-AUC 0.707; the high-recall training threshold produces 93.0% recall with low specificity.  
**Decision value.** Choose contact thresholds consistent with capacity and false-positive/false-negative costs.  
**Primary limitation.** Use only as an educational propensity analysis; real campaigns require consent, fairness review, frequency limits, and current validation.

![Primary evidence](reports/figures/holiday_propensity_evidence.png)

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<https://github.com/unit-mole/Holiday_Package_Prediction>)

## Business problem

The intended user is **A travel-campaign analyst**. The analysis supports this decision: **Choose contact thresholds consistent with capacity and false-positive/false-negative costs.** It does not claim causality or production readiness unless the study design supports that claim.

## Analytical questions and success criteria

1. What data-quality issues materially affect the analysis?
2. Which baseline establishes the minimum useful performance or descriptive reference?
3. Which method is selected under a leakage-safe validation design?
4. How stable, calibrated, or assumption-sensitive is the result?
5. What action is supported, and what action remains outside scope?

Technical success requires a fully executed pipeline, correct split logic, task-appropriate metrics, saved evidence, deterministic seeds where supported, and zero notebook errors. Business success requires an interpretable result that changes a defensible analytical decision without fabricating financial impact.

## Dataset and provenance

872 records with purchase outcome, salary, age, education, children, and foreign-status fields.

Bundled in the original repository; collection population, time period, and reuse terms are not documented.

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

## Methodology

Stratified CV, prevalence baseline, logistic/LDA/tree/forest/boosting comparison, probability calibration, training-only threshold selection, PR-AUC, ROC-AUC, customer profiling, and permutation importance.

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

## Validation strategy

```json
{
  "train_rows": 654,
  "untouched_test_rows": 218,
  "selection": "5-fold stratified CV on training data",
  "selection_metric": "PR-AUC",
  "random_seed": 42
}
```

## Verified result

> Calibrated logistic regression reaches untouched-test ROC-AUC 0.730 and PR-AUC 0.707; the high-recall training threshold produces 93.0% recall with low specificity.

### Primary comparison table

| model | cv_pr_auc_mean | cv_pr_auc_std | cv_roc_auc_mean | cv_balanced_accuracy_mean |
|---|---|---|---|---|
| logistic_regression | 0.714 | 0.032 | 0.724 | 0.664 |
| gradient_boosting | 0.710 | 0.050 | 0.736 | 0.661 |
| linear_discriminant_analysis | 0.708 | 0.031 | 0.721 | 0.658 |
| random_forest | 0.699 | 0.043 | 0.728 | 0.676 |
| decision_tree | 0.636 | 0.021 | 0.691 | 0.629 |
| dummy_prevalence | 0.460 | 0.003 | 0.500 | 0.500 |

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
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | Calibrated logistic regression reaches untouched-test ROC-AUC 0.730 and PR-AUC 0.707; the high-recall training threshold produces 93.0% recall with low specificity. | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
| 2 | Review the largest error, uncertainty, or sensitivity segment before deployment. | See saved diagnostic tables | Reduces hidden failure risk | Small subgroups can produce unstable estimates | Track subgroup error and interval coverage |
| 3 | Keep a transparent baseline in future monitoring. | Baseline comparison is recorded in the notebook | Detects when complexity stops adding value | Baselines do not capture every business driver | Compare every refresh against the same baseline |

## Limitations and responsible use

See the executed metrics for project-specific limitations.

Use only as an educational propensity analysis; real campaigns require consent, fairness review, frequency limits, and current validation.

## Repository structure

```text
06-holiday-package-prediction/
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
python projects/06-holiday-package-prediction/src/analysis.py
python scripts/execute_notebooks.py --project 06-holiday-package-prediction
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/06-holiday-package-prediction/reports/` and, for selected predictive models, `projects/06-holiday-package-prediction/models/`.

## Technologies and skills demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Binary propensity modeling · reproducibility · responsible interpretation.

## Future work

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

## Interview-ready explanation

“I rebuilt this as a binary propensity modeling case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.”

## Résumé bullets

- Re-engineered a travel marketing analysis into a reproducible binary propensity modeling workflow with automated data-quality evidence, saved outputs, and a fully executed recruiter-facing notebook.
- Implemented stratified cv and problem-appropriate validation to produce the verified result: Calibrated logistic regression reaches untouched-test ROC-AUC 0.730 and PR-AUC 0.707; the high-recall training threshold produces 93.0% recall with low specificity.
- Translated model/statistical diagnostics into prioritized recommendations while documenting provenance, uncertainty, and responsible-use limits.
