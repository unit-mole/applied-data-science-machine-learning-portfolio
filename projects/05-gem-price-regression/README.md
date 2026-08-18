# Cubic Zirconia Price Modeling

> **Value proposition:** Compare interpretable and nonlinear price models, diagnose residual risk, and quantify empirical prediction coverage.

![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg) ![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg) ![Notebook](https://img.shields.io/badge/Notebook-Executed-F37626.svg)

## Executive summary

**Business question.** Compare interpretable and nonlinear price models, diagnose residual risk, and quantify empirical prediction coverage.  
**Dataset.** 26,967 cubic-zirconia records with physical measurements, quality grades, and price.  
**Verified result.** Histogram gradient boosting reaches untouched-test R² 0.981, RMSE 562, and 90.7% coverage for the training-calibrated 90% diagnostic interval.  
**Decision value.** Estimate price ranges and identify where prediction errors become operationally material.  
**Primary limitation.** See limitations below.

![Primary evidence](reports/figures/gem_price_model_evidence.png)

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<https://github.com/unit-mole/Gems-Prediction-using-Linear-Regression>)

## Business problem

The intended user is **A merchandising, pricing, or appraisal analyst**. The analysis supports this decision: **Estimate price ranges and identify where prediction errors become operationally material.** It does not claim causality or production readiness unless the study design supports that claim.

## Analytical questions and success criteria

1. What data-quality issues materially affect the analysis?
2. Which baseline establishes the minimum useful performance or descriptive reference?
3. Which method is selected under a leakage-safe validation design?
4. How stable, calibrated, or assumption-sensitive is the result?
5. What action is supported, and what action remains outside scope?

Technical success requires a fully executed pipeline, correct split logic, task-appropriate metrics, saved evidence, deterministic seeds where supported, and zero notebook errors. Business success requires an interpretable result that changes a defensible analytical decision without fabricating financial impact.

## Dataset and provenance

26,967 cubic-zirconia records with physical measurements, quality grades, and price.

Bundled in the original repository; market period, price units, sampling context, and redistribution terms are not fully documented.

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

## Methodology

Leakage-safe imputation/encoding, median baseline, linear and regularized log-target models, random forest, histogram boosting, cross-validation, residual diagnostics, permutation importance, segment errors, and calibration-residual intervals.

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

## Validation strategy

```json
{
  "training_rows": 21573,
  "untouched_test_rows": 5394,
  "model_selection": "4-fold shuffled CV on training only",
  "calibration_rows_for_interval": 4315,
  "random_seed": 42
}
```

## Verified result

> Histogram gradient boosting reaches untouched-test R² 0.981, RMSE 562, and 90.7% coverage for the training-calibrated 90% diagnostic interval.

### Primary comparison table

| model | cv_rmse_mean | cv_rmse_std | cv_mae_mean | cv_r_squared_mean |
|---|---|---|---|---|
| hist_gradient_boosting | 574.150 | 32.578 | 299.893 | 0.979 |
| random_forest | 594.728 | 27.049 | 298.884 | 0.978 |
| log_target_ridge | 921.811 | 81.047 | 443.555 | 0.947 |
| linear_regression | 1128.547 | 31.882 | 742.037 | 0.921 |
| median_baseline | 4293.919 | 49.744 | 2815.658 | -0.150 |

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
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | Histogram gradient boosting reaches untouched-test R² 0.981, RMSE 562, and 90.7% coverage for the training-calibrated 90% diagnostic interval. | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
| 2 | Review the largest error, uncertainty, or sensitivity segment before deployment. | See saved diagnostic tables | Reduces hidden failure risk | Small subgroups can produce unstable estimates | Track subgroup error and interval coverage |
| 3 | Keep a transparent baseline in future monitoring. | Baseline comparison is recorded in the notebook | Detects when complexity stops adding value | Baselines do not capture every business driver | Compare every refresh against the same baseline |

## Limitations and responsible use

See the executed metrics for project-specific limitations.

Treat outputs as educational analytical evidence and require domain review before operational use.

## Repository structure

```text
05-gem-price-regression/
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
python projects/05-gem-price-regression/src/analysis.py
python scripts/execute_notebooks.py --project 05-gem-price-regression
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/05-gem-price-regression/reports/` and, for selected predictive models, `projects/05-gem-price-regression/models/`.

## Technologies and skills demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Supervised regression · reproducibility · responsible interpretation.

## Future work

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

## Interview-ready explanation

“I rebuilt this as a supervised regression case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.”

## Résumé bullets

- Re-engineered a retail pricing and appraisal analytics analysis into a reproducible supervised regression workflow with automated data-quality evidence, saved outputs, and a fully executed recruiter-facing notebook.
- Implemented leakage-safe imputation/encoding and problem-appropriate validation to produce the verified result: Histogram gradient boosting reaches untouched-test R² 0.981, RMSE 562, and 90.7% coverage for the training-calibrated 90% diagnostic interval.
- Translated model/statistical diagnostics into prioritized recommendations while documenting provenance, uncertainty, and responsible-use limits.
