# Cafe Marketing and Retail Analytics

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Modeling-f7931e.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Executed%20Notebook-f37626.svg)](notebooks/01_end_to_end_analysis.ipynb)
[![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg)](../../REPRODUCIBILITY_REPORT.md)
[![License](https://img.shields.io/badge/Code%20License-MIT-green.svg)](../../LICENSE)

> **Value proposition:** Translate point-of-sale lines into revenue, order, daypart, basket, and stable menu-item insights supported by available fields.



---

## Project Overview

**Business question.** Translate point-of-sale lines into revenue, order, daypart, basket, and stable menu-item insights supported by available fields.  
**Dataset.** 145,830 cafe line items covering 69,982 bills and one year of activity.  
**Verified result.** The cleaned year contains 69,982 bills and 32,654,640 recorded revenue units; two stable menu-item groups score 0.395 silhouette.  
**Decision value.** Prioritize menu review, daypart staffing, and carefully tested cross-sell ideas.  
**Primary limitation.** There is no customer identifier, so customer-level RFM, retention, and lifetime-value claims are not possible from this dataset.

![Primary evidence](reports/figures/cafe_business_evidence.png)

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<https://github.com/unit-mole/Marketing_and_Retail_Analysis>)

---

## Responsible Use

There is no customer identifier, so customer-level RFM, retention, and lifetime-value claims are not possible from this dataset.

Treat outputs as educational analytical evidence and require domain review before operational use.

This project is intended for education, analytical demonstration, and portfolio presentation. Its outputs should be reviewed by qualified domain experts before they influence operational, financial, medical, quality, or other consequential decisions.

---

## Business Problem

The intended user is **A cafe operator or marketing analyst**. The analysis supports this decision: **Prioritize menu review, daypart staffing, and carefully tested cross-sell ideas.** It does not claim causality or production readiness unless the study design supports that claim.

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

145,830 cafe line items covering 69,982 bills and one year of activity.

Bundled in the original repository; business identity, geography, currency, and redistribution terms are not documented.

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

---

## Tools and Technologies

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Transactional business analysis and item segmentation · reproducibility · responsible interpretation.

---

## End-to-End Project Workflow

Duplicate control, monthly/category/daypart KPIs, order-value analysis, bill-level pair support/confidence/lift, and stable K-means menu-item segmentation.

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

---

## Model and Analytical Results

> The cleaned year contains 69,982 bills and 32,654,640 recorded revenue units; two stable menu-item groups score 0.395 silhouette.

### Primary comparison table

| item_1 | item_2 | joint_bills | support | confidence_1_to_2 | confidence_2_to_1 | lift |
|---|---|---|---|---|---|---|
| ADD FRIES                      | B.M.T. PANINI                  | 151 | 0.002 | 0.201 | 0.058 | 5.394 |
| B.M.T. PANINI                  | MAGGI NDL ARRABIATA            | 134 | 0.002 | 0.051 | 0.152 | 4.086 |
| RED BULL 2+1                   | SAMBUCA                        | 290 | 0.004 | 0.249 | 0.066 | 3.932 |
| MAGGI NDL ARRABIATA            | SAMBUCA                        | 175 | 0.003 | 0.199 | 0.040 | 3.143 |
| CALCUTTA MINT                  | RED BULL 2+1                   | 166 | 0.002 | 0.050 | 0.142 | 3.010 |
| B.M.T. PANINI                  | PHILLYCREAM CHEESE &CHILLY PAN | 183 | 0.003 | 0.070 | 0.098 | 2.643 |
| RED BULL ENERGY DRINK          | SAMBUCA                        | 283 | 0.004 | 0.152 | 0.064 | 2.407 |
| N R G  HOOKAH                  | RED BULL ENERGY DRINK          | 141 | 0.002 | 0.063 | 0.076 | 2.374 |
| B.M.T. PANINI                  | KIT KAT SHAKE                  | 148 | 0.002 | 0.057 | 0.088 | 2.368 |
| B.M.T. PANINI                  | COTTAGE CHEESE PANINI          | 141 | 0.002 | 0.054 | 0.087 | 2.350 |

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
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | The cleaned year contains 69,982 bills and 32,654,640 recorded revenue units; two stable menu-item groups score 0.395 silhouette. | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
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
python projects/10-marketing-retail-analysis/src/analysis.py
python scripts/execute_notebooks.py --project 10-marketing-retail-analysis
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/10-marketing-retail-analysis/reports/` and, for selected predictive models, `projects/10-marketing-retail-analysis/models/`.

---

## Project Structure

```text
10-marketing-retail-analysis/
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

There is no customer identifier, so customer-level RFM, retention, and lifetime-value claims are not possible from this dataset.

Treat outputs as educational analytical evidence and require domain review before operational use.

---

## Future Improvements

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

---

## Skills Demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Transactional business analysis and item segmentation · reproducibility · responsible interpretation.

---

## Portfolio Positioning

I rebuilt this as a transactional business analysis and item segmentation case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.

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
