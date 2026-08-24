# Wine Sales Forecasting with Rolling-Origin Validation

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Modeling-f7931e.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Executed%20Notebook-f37626.svg)](notebooks/01_end_to_end_analysis.ipynb)
[![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg)](../../REPRODUCIBILITY_REPORT.md)
[![License](https://img.shields.io/badge/Code%20License-MIT-green.svg)](../../LICENSE)

> **Value proposition:** Select transparent monthly forecasting methods on multiple historical origins and evaluate once on a final 24-month holdout.



---

## Project Overview

**Business question.** Select transparent monthly forecasting methods on multiple historical origins and evaluate once on a final 24-month holdout.  
**Dataset.** 187 monthly Rose and Sparkling observations from January 1980 through July 1995.  
**Verified result.** Rolling-origin selection chooses trend plus month for Rose (holdout RMSE 13.6) and additive Holt-Winters for Sparkling (RMSE 358.7).  
**Decision value.** Choose a reproducible baseline and quantify forecast risk before inventory commitment.  
**Primary limitation.** The series ends in 1995 and lacks price, promotion, inventory, weather, and economic drivers; diagnostic intervals are empirical validation-error bands rather than formal probabilistic intervals.

![Primary evidence](reports/figures/wine_forecasting_evidence.png)

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<https://github.com/unit-mole/Forecasting_Wine_Sales_for_ABC_Estate_Wines_company>)

---

## Responsible Use

The series ends in 1995 and lacks price, promotion, inventory, weather, and economic drivers; diagnostic intervals are empirical validation-error bands rather than formal probabilistic intervals.

Treat outputs as educational analytical evidence and require domain review before operational use.

This project is intended for education, analytical demonstration, and portfolio presentation. Its outputs should be reviewed by qualified domain experts before they influence operational, financial, medical, quality, or other consequential decisions.

---

## Business Problem

The intended user is **An inventory or demand-planning analyst**. The analysis supports this decision: **Choose a reproducible baseline and quantify forecast risk before inventory commitment.** It does not claim causality or production readiness unless the study design supports that claim.

---

## Project Objective

1. What data-quality issues materially affect the analysis?
2. Which baseline establishes the minimum useful performance or descriptive reference?
3. Which method is selected under a leakage-safe validation design?
4. How stable, calibrated, or assumption-sensitive is the result?
5. What action is supported, and what action remains outside scope?

Technical success requires a fully executed pipeline, correct split logic, task-appropriate metrics, saved evidence, deterministic seeds where supported, and zero notebook errors. Business success requires an interpretable result that changes a defensible analytical decision without fabricating financial impact.

---

## Project Pattern

This project follows a reproducible applied-data-science pattern:

1. establish dataset provenance and data-quality constraints;
2. define the analytical question and minimum useful baseline;
3. select a validation strategy that respects the unit of observation;
4. compare justified statistical or machine-learning methods;
5. preserve results, diagnostics, and reproducibility evidence;
6. translate the findings into a bounded business recommendation;
7. document limitations, licensing, and responsible-use conditions.

---

## Dataset

187 monthly Rose and Sparkling observations from January 1980 through July 1995.

Bundled in the original repository; commercial source, currency/units, and redistribution terms are not documented.

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

---

## Tools and Technologies

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Monthly time-series forecasting · reproducibility · responsible interpretation.

---

## End-to-End Project Workflow

Frequency audit, train-contained interpolation, seasonal-naive baseline, trend/month regression, lagged ridge, additive Holt-Winters implementation, three rolling origins, empirical intervals, and Ljung–Box residual autocorrelation.

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

---

## Model and Analytical Results

> Rolling-origin selection chooses trend plus month for Rose (holdout RMSE 13.6) and additive Holt-Winters for Sparkling (RMSE 358.7).

### Primary comparison table

| product | fold | model | mae | rmse | r_squared | mape_percent |
|---|---|---|---|---|---|---|
| rose | 1 | seasonal_naive | 9.833 | 11.467 | 0.754 | 14.554 |
| rose | 1 | trend_plus_month | 11.847 | 14.072 | 0.630 | 16.213 |
| rose | 1 | ridge_lag_1_12 | 13.676 | 14.473 | 0.608 | 19.662 |
| rose | 1 | holt_winters__0.2_0.05_0.2 | 10.991 | 12.839 | 0.692 | 14.259 |
| rose | 1 | holt_winters__0.3_0.1_0.3 | 11.027 | 12.653 | 0.701 | 15.136 |
| rose | 1 | holt_winters__0.5_0.1_0.2 | 17.177 | 20.183 | 0.238 | 23.614 |
| rose | 2 | seasonal_naive | 15.583 | 18.355 | -0.161 | 25.962 |
| rose | 2 | trend_plus_month | 6.640 | 10.050 | 0.652 | 10.018 |
| rose | 2 | ridge_lag_1_12 | 18.041 | 19.528 | -0.314 | 34.246 |
| rose | 2 | holt_winters__0.2_0.05_0.2 | 17.528 | 19.171 | -0.266 | 29.093 |

All values above are generated from the committed data and synchronized with `reports/metrics.json` after execution.

---

## Evaluation, Explainability, and Robustness

- The project saves its comparison and diagnostic tables under `reports/tables/`.
- The primary figure combines model/statistical evidence with error, stability, calibration, or profile evidence appropriate to the task.
- Predictive projects compare against a baseline and preserve an untouched holdout.
- Statistical projects report assumptions, effect size, and robust alternatives.
- Clustering projects report internal metrics as descriptive evidence—not proof of objectively real groups.
- Time-series projects use chronological origins and transparent baselines.

---

## Business Recommendations

| Priority | Recommendation | Evidence | Expected benefit | Risk or limitation | How to measure success |
|---:|---|---|---|---|---|
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | Rolling-origin selection chooses trend plus month for Rose (holdout RMSE 13.6) and additive Holt-Winters for Sparkling (RMSE 358.7). | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
| 2 | Review the largest error, uncertainty, or sensitivity segment before deployment. | See saved diagnostic tables | Reduces hidden failure risk | Small subgroups can produce unstable estimates | Track subgroup error and interval coverage |
| 3 | Keep a transparent baseline in future monitoring. | Baseline comparison is recorded in the notebook | Detects when complexity stops adding value | Baselines do not capture every business driver | Compare every refresh against the same baseline |

---

## Model and Evaluation Artifacts

The committed project preserves its analytical evidence through:

- the fully executed notebook under `notebooks/`;
- reusable analytical logic under `src/`;
- synchronized metrics in `reports/metrics.json`;
- comparison and diagnostic tables under `reports/tables/`;
- recruiter-facing figures under `reports/figures/`;
- fitted artifacts under `models/` when a saved model is appropriate;
- project-level provenance documentation under `data/README.md`.

---

## Run the Project Locally

From the portfolio root:

```bash
python projects/09-wine-sales-forecasting/src/analysis.py
python scripts/execute_notebooks.py --project 09-wine-sales-forecasting
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/09-wine-sales-forecasting/reports/` and, for selected predictive models, `projects/09-wine-sales-forecasting/models/`.

---

## Project Structure

```text
09-wine-sales-forecasting/
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

---

## Limitations

The series ends in 1995 and lacks price, promotion, inventory, weather, and economic drivers; diagnostic intervals are empirical validation-error bands rather than formal probabilistic intervals.

Treat outputs as educational analytical evidence and require domain review before operational use.

---

## Future Improvements

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

---

## Skills Demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Monthly time-series forecasting · reproducibility · responsible interpretation.

---

## Portfolio Positioning

I rebuilt this as a monthly time-series forecasting case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.

---

## Data and Third-Party Materials

The original source code and original documentation created for this project are licensed under the portfolio's [MIT License](../../LICENSE).

The datasets, pretrained models, model weights, images, reference materials, and other third-party assets used by this project are **not** relicensed under the MIT License. They remain subject to the licenses, source terms, attribution requirements, and usage restrictions established by their respective owners.

Dataset provenance and known reuse limitations are documented in the [project data documentation](data/README.md) and in the Dataset section above. Where the upstream collection process or redistribution terms are undocumented, users must not assume that the material is cleared for unrestricted reuse. Review the original provider's terms before copying, redistributing, or using any third-party material outside this portfolio.

Unless explicitly stated otherwise, trained models, analytical outputs, reports, and generated artifacts are provided for educational, research, and portfolio-demonstration purposes. They are not guaranteed to be suitable for production, medical, financial, safety-critical, or other high-risk applications.

---

## Author

**Anmol Tripathi**  
Quality Data Scientist | Data Science | Machine Learning | Applied AI | Statistical Analysis | Predictive Analytics | Analytics Engineering | Quality Analytics
