# Salary Factor Analysis and College Admissions PCA

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Modeling-f7931e.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Executed%20Notebook-f37626.svg)](notebooks/01_end_to_end_analysis.ipynb)
[![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg)](../../REPRODUCIBILITY_REPORT.md)
[![License](https://img.shields.io/badge/Code%20License-MIT-green.svg)](../../LICENSE)

> **Value proposition:** Assess salary differences with robust sensitivity checks and compress correlated college indicators without hiding information loss.



---

## Project Overview

**Business question.** Assess salary differences with robust sensitivity checks and compress correlated college indicators without hiding information loss.  
**Dataset.** 40 salary observations and 777 colleges with 17 numeric admissions and institutional indicators.  
**Verified result.** Education shows a large observed salary association (eta²=0.626); 6 standardized components retain at least 80% of college-indicator variance.  
**Decision value.** Identify material group differences and select a defensible reduced indicator set.  
**Primary limitation.** The salary sample has only 40 observational records; robust alternatives and corrected pairwise tests reduce but do not eliminate small-sample and design limitations.

![Primary evidence](reports/figures/anova_pca_evidence.png)

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<https://github.com/unit-mole/Salary-Analysis-using-ANOVA-and-Principal-Component-Analysis-on-College-Admissions-Data>)

---

## Responsible Use

The salary sample has only 40 observational records; robust alternatives and corrected pairwise tests reduce but do not eliminate small-sample and design limitations.

Treat outputs as educational analytical evidence and require domain review before operational use.

This project is intended for education, analytical demonstration, and portfolio presentation. Its outputs should be reviewed by qualified domain experts before they influence operational, financial, medical, quality, or other consequential decisions.

---

## Business Problem

The intended user is **A compensation analyst or higher-education analyst**. The analysis supports this decision: **Identify material group differences and select a defensible reduced indicator set.** It does not claim causality or production readiness unless the study design supports that claim.

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

40 salary observations and 777 colleges with 17 numeric admissions and institutional indicators.

College data corresponds to the ISLR College dataset; the small salary dataset's sampling process and license are not documented.

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

---

## Tools and Technologies

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Factorial inference and dimensionality reduction · reproducibility · responsible interpretation.

---

## End-to-End Project Workflow

Classic and Welch ANOVA, Kruskal sensitivity, Levene test, eta-squared, Holm-corrected pairwise Welch tests, interaction F-test, standardized PCA, loading interpretation, and reconstruction error.

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

---

## Model and Analytical Results

> Education shows a large observed salary association (eta²=0.626); 6 standardized components retain at least 80% of college-indicator variance.

### Primary comparison table

| field | group_1 | group_2 | mean_difference | cohen_d | welch_p_value | holm_adjusted_p_value |
|---|---|---|---|---|---|---|
| Education |  Bachelors |  Doctorate | -43274.067 | -0.966 | 0.012 | 0.012 |
| Education |  Bachelors |  HS-grad | 90114.156 | 2.308 | 0.000 | 0.000 |
| Education |  Doctorate |  HS-grad | 133388.222 | 3.635 | 0.000 | 0.000 |
| Occupation |  Adm-clerical |  Exec-managerial | -55693.300 | -1.271 | 0.011 | 0.064 |
| Occupation |  Adm-clerical |  Prof-specialty | -27528.854 | -0.412 | 0.314 | 0.983 |
| Occupation |  Adm-clerical |  Sales | -16180.117 | -0.256 | 0.545 | 1.000 |
| Occupation |  Exec-managerial |  Prof-specialty | 28164.446 | 0.418 | 0.246 | 0.983 |
| Occupation |  Exec-managerial |  Sales | 39513.183 | 0.631 | 0.105 | 0.527 |
| Occupation |  Prof-specialty |  Sales | 11348.737 | 0.152 | 0.707 | 1.000 |

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
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | Education shows a large observed salary association (eta²=0.626); 6 standardized components retain at least 80% of college-indicator variance. | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
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
python projects/03-anova-pca-analysis/src/analysis.py
python scripts/execute_notebooks.py --project 03-anova-pca-analysis
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/03-anova-pca-analysis/reports/` and, for selected predictive models, `projects/03-anova-pca-analysis/models/`.

---

## Project Structure

```text
03-anova-pca-analysis/
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

The salary sample has only 40 observational records; robust alternatives and corrected pairwise tests reduce but do not eliminate small-sample and design limitations.

Treat outputs as educational analytical evidence and require domain review before operational use.

---

## Future Improvements

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

---

## Skills Demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Factorial inference and dimensionality reduction · reproducibility · responsible interpretation.

---

## Portfolio Positioning

I rebuilt this as a factorial inference and dimensionality reduction case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.

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
