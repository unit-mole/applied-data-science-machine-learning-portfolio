# Online Retail Customer Segmentation

> **Value proposition:** Create auditable customer profiles after explicit cancellation, return, duplicate, and missing-ID treatment.

![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg) ![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg) ![Notebook](https://img.shields.io/badge/Notebook-Executed-F37626.svg)

## Executive summary

**Business question.** Create auditable customer profiles after explicit cancellation, return, duplicate, and missing-ID treatment.  
**Dataset.** 541,909 UCI Online Retail transaction rows from December 2010 through December 2011.  
**Verified result.** The pipeline segments 4,338 customers into 2 stable RFM groups (silhouette 0.432, seed ARI 0.999).  
**Decision value.** Design differentiated retention and reactivation experiments without sensitive profiling.  
**Primary limitation.** Segments describe historical purchasing behavior and must not support discriminatory pricing, credit decisions, or sensitive profiling.

![Primary evidence](reports/figures/online_retail_segmentation_evidence.png)

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<https://github.com/unit-mole/Customer_segmentaion_online_Retail>)

## Business problem

The intended user is **An e-commerce CRM or retention analyst**. The analysis supports this decision: **Design differentiated retention and reactivation experiments without sensitive profiling.** It does not claim causality or production readiness unless the study design supports that claim.

## Analytical questions and success criteria

1. What data-quality issues materially affect the analysis?
2. Which baseline establishes the minimum useful performance or descriptive reference?
3. Which method is selected under a leakage-safe validation design?
4. How stable, calibrated, or assumption-sensitive is the result?
5. What action is supported, and what action remains outside scope?

Technical success requires a fully executed pipeline, correct split logic, task-appropriate metrics, saved evidence, deterministic seeds where supported, and zero notebook errors. Business success requires an interpretable result that changes a defensible analytical decision without fabricating financial impact.

## Dataset and provenance

541,909 UCI Online Retail transaction rows from December 2010 through December 2011.

UCI Online Retail dataset; preserve UCI attribution and verify source-specific reuse terms before redistribution.

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

## Methodology

Transaction cleaning, customer-level RFM, log scaling, K-means/Gaussian-mixture comparison, silhouette/Davies–Bouldin/Calinski–Harabasz metrics, seed stability, outlier sensitivity, PCA, and evidence-based naming.

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

## Validation strategy

```json
{
  "methods": [
    "K-means",
    "Gaussian mixture"
  ],
  "candidate_clusters": [
    2,
    3,
    4,
    5,
    6,
    7
  ],
  "selection_rule": "composite rank among K-means candidates with >=5% smallest segment and >=0.80 seed ARI",
  "selected_clusters": 2,
  "selected_silhouette": 0.4323284246768482,
  "selected_davies_bouldin": 0.8924990931024944,
  "selected_calinski_harabasz": 4367.323097619211,
  "selected_seed_stability_ari": 0.9990752738031528
}
```

## Verified result

> The pipeline segments 4,338 customers into 2 stable RFM groups (silhouette 0.432, seed ARI 0.999).

### Primary comparison table

| method | clusters | silhouette | davies_bouldin | calinski_harabasz | mean_seed_stability_ari | smallest_cluster_share |
|---|---|---|---|---|---|---|
| kmeans | 2 | 0.432 | 0.892 | 4367.323 | 0.999 | 0.384 |
| gaussian_mixture | 2 | 0.289 | 1.067 | 2288.485 |  | 0.344 |
| kmeans | 3 | 0.337 | 1.048 | 3625.303 | 0.997 | 0.177 |
| gaussian_mixture | 3 | 0.260 | 1.217 | 2795.227 |  | 0.203 |
| kmeans | 4 | 0.337 | 1.011 | 3328.919 | 0.970 | 0.163 |
| gaussian_mixture | 4 | 0.173 | 1.722 | 2148.459 |  | 0.192 |
| kmeans | 5 | 0.316 | 0.988 | 3192.977 | 0.944 | 0.078 |
| gaussian_mixture | 5 | 0.155 | 1.778 | 1892.051 |  | 0.046 |
| kmeans | 6 | 0.312 | 1.016 | 3082.355 | 0.956 | 0.074 |
| gaussian_mixture | 6 | 0.123 | 2.181 | 1496.656 |  | 0.022 |

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
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | The pipeline segments 4,338 customers into 2 stable RFM groups (silhouette 0.432, seed ARI 0.999). | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
| 2 | Review the largest error, uncertainty, or sensitivity segment before deployment. | See saved diagnostic tables | Reduces hidden failure risk | Small subgroups can produce unstable estimates | Track subgroup error and interval coverage |
| 3 | Keep a transparent baseline in future monitoring. | Baseline comparison is recorded in the notebook | Detects when complexity stops adding value | Baselines do not capture every business driver | Compare every refresh against the same baseline |

## Limitations and responsible use

See the executed metrics for project-specific limitations.

Segments describe historical purchasing behavior and must not support discriminatory pricing, credit decisions, or sensitive profiling.

## Repository structure

```text
12-online-retail-segmentation/
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
python projects/12-online-retail-segmentation/src/analysis.py
python scripts/execute_notebooks.py --project 12-online-retail-segmentation
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/12-online-retail-segmentation/reports/` and, for selected predictive models, `projects/12-online-retail-segmentation/models/`.

## Technologies and skills demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · Unsupervised RFM segmentation · reproducibility · responsible interpretation.

## Future work

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

## Interview-ready explanation

“I rebuilt this as a unsupervised rfm segmentation case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.”

## Résumé bullets

- Re-engineered a e-commerce customer analytics analysis into a reproducible unsupervised rfm segmentation workflow with automated data-quality evidence, saved outputs, and a fully executed recruiter-facing notebook.
- Implemented transaction cleaning and problem-appropriate validation to produce the verified result: The pipeline segments 4,338 customers into 2 stable RFM groups (silhouette 0.432, seed ARI 0.999).
- Translated model/statistical diagnostics into prioritized recommendations while documenting provenance, uncertainty, and responsible-use limits.
