# Applied Data Science & Machine Learning Portfolio

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243.svg)](https://numpy.org/)
[![pandas](https://img.shields.io/badge/pandas-2.x-150458.svg)](https://pandas.pydata.org/)
[![SciPy](https://img.shields.io/badge/SciPy-Scientific%20Computing-8CAAE6.svg)](https://scipy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-13%20Executed%20Notebooks-F37626.svg)](https://jupyter.org/)
[![Portfolio](https://img.shields.io/badge/Portfolio-13%2F13%20Completed-2ea44f.svg)](#completed-projects)
[![Validation](https://img.shields.io/badge/Validation-13%20Passed-2ea44f.svg)](PROJECT_STATUS_MATRIX.md)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Python%203.12%20%7C%203.13-2088ff.svg)](https://github.com/unit-mole/applied-data-science-machine-learning-portfolio/actions)
[![License](https://img.shields.io/badge/Code%20License-MIT-green.svg)](LICENSE)

A structured portfolio of **13 completed and fully executed data science projects** covering statistical inference, exploratory analysis, regression, classification, clustering, principal component analysis, natural language processing, time-series forecasting, retail analytics, biomedical machine learning, customer segmentation, and historical public-health forecasting.

Each project is developed as an end-to-end case study with reproducible source code, an executed notebook, task-appropriate validation, saved results, professional documentation, and transparent responsible-use boundaries.

**Portfolio status:** 13 completed projects · 13 executed notebooks · 13 validated result packages  
**Repository owner:** [Anmol Tripathi](https://github.com/unit-mole)  
**Runtime support:** Python 3.12 and Python 3.13  
**Last complete acceptance run:** 13 projects passed · 7 automated tests passed · 0 notebook errors

---

## Portfolio Objective

This repository demonstrates how statistics, data science, and machine learning can be used to convert raw data into defensible analytical findings and practical decisions.

The portfolio intentionally moves beyond assignment-style notebooks. Every project follows a consistent professional workflow:

> **Problem definition → data provenance → quality audit → exploratory analysis → hypotheses → feature engineering → baseline → candidate comparison → validation → explainability → decision guidance → limitations**

Depending on the task, a project contains:

- a clearly defined analytical or business problem;
- documented datasets, schemas, checksums, and provenance limitations;
- data-quality checks and explicit cleaning decisions;
- statistical assumptions or leakage-safe preprocessing;
- simple baselines and meaningful candidate comparisons;
- training-only, grouped, or chronological model selection;
- untouched holdout evaluation where appropriate;
- task-aligned metrics, diagnostics, and sensitivity analysis;
- saved tables, charts, structured metrics, and reusable model artifacts;
- a fully executed notebook whose outputs render directly on GitHub;
- modular Python source code and shared utilities;
- automated repository validation for Python 3.12 and 3.13;
- responsible-use guidance and transparent limitations.

The portfolio demonstrates skills relevant to:

- Data Science;
- Machine Learning;
- Statistical Analysis;
- Predictive Analytics;
- Customer and Retail Analytics;
- Time-Series Forecasting;
- Natural Language Processing;
- Quality Analytics;
- Analytics Engineering;
- Model Evaluation and Governance.

---

## Completed Projects

| No. | Project | Analytical problem | Verified result | Evidence | Status |
|---:|---|---|---|---|---|
| 1 | [Statistical Methods for Decision-Making](projects/01-statistical-methods/) | Statistical inference and operational decisions | Shingle B is below the 0.35 specification limit (`p=0.0021`); Shingle A does not pass the prespecified t-test (`p=0.0748`). | [Notebook](projects/01-statistical-methods/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/01-statistical-methods/reports/figures/statistical_decision_evidence.png) | Completed |
| 2 | [Uber Drive Behavior Analysis](projects/02-uber-drive-analysis/) | Trip-pattern and productivity analysis | 1,154 valid trips total 12,194.8 miles; 94.1% of recorded mileage is categorized as business. | [Notebook](projects/02-uber-drive-analysis/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/02-uber-drive-analysis/reports/figures/uber_trip_behavior_evidence.png) | Completed |
| 3 | [Salary ANOVA and College Admissions PCA](projects/03-anova-pca-analysis/) | Factorial inference and dimensionality reduction | Education has a large observed salary association (`eta²=0.626`); six PCs retain at least 80% of standardized variance. | [Notebook](projects/03-anova-pca-analysis/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/03-anova-pca-analysis/reports/figures/anova_pca_evidence.png) | Completed |
| 4 | [Insurance Claim Propensity Modeling](projects/04-insurance-claim-prediction/) | Imbalanced binary classification | Tuned random forest: test ROC-AUC `0.800`, PR-AUC `0.618`, balanced accuracy `0.709`. | [Notebook](projects/04-insurance-claim-prediction/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/04-insurance-claim-prediction/reports/figures/insurance_model_evidence.png) | Completed |
| 5 | [Cubic Zirconia Price Modeling](projects/05-gem-price-regression/) | Supervised regression | Histogram gradient boosting: test R² `0.981`, RMSE `562.0`; diagnostic 90% interval coverage `90.7%`. | [Notebook](projects/05-gem-price-regression/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/05-gem-price-regression/reports/figures/gem_price_model_evidence.png) | Completed |
| 6 | [Holiday Package Purchase Propensity](projects/06-holiday-package-prediction/) | Binary propensity modeling | Calibrated logistic regression: test ROC-AUC `0.730`, PR-AUC `0.707`; high-recall threshold reaches `93.0%` recall. | [Notebook](projects/06-holiday-package-prediction/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/06-holiday-package-prediction/reports/figures/holiday_propensity_evidence.png) | Completed |
| 7 | [Retrospective Election Survey Classification](projects/07-election-exit-poll-prediction/) | Historical respondent classification | Calibrated random forest: test ROC-AUC `0.907`, balanced accuracy `0.800`. | [Notebook](projects/07-election-exit-poll-prediction/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/07-election-exit-poll-prediction/reports/figures/election_model_evidence.png) | Completed |
| 8 | [U.S. Presidential Speech Analysis](projects/08-presidential-speech-analysis/) | Small-corpus exploratory NLP | Kennedy 1961 and Nixon 1973 are the most similar tested pair by unigram/bigram TF-IDF cosine similarity (`0.114`). | [Notebook](projects/08-presidential-speech-analysis/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/08-presidential-speech-analysis/reports/figures/speech_analysis_evidence.png) | Completed |
| 9 | [Wine Sales Forecasting](projects/09-wine-sales-forecasting/) | Rolling-origin monthly forecasting | Rose holdout RMSE `13.6`; Sparkling holdout RMSE `358.7` and R² `0.932`. | [Notebook](projects/09-wine-sales-forecasting/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/09-wine-sales-forecasting/reports/figures/wine_forecasting_evidence.png) | Completed |
| 10 | [Cafe Marketing and Retail Analytics](projects/10-marketing-retail-analysis/) | Transaction analytics, basket analysis, and item segmentation | 69,982 bills and 32.65M recorded revenue units; two stable menu groups with silhouette `0.395`. | [Notebook](projects/10-marketing-retail-analysis/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/10-marketing-retail-analysis/reports/figures/cafe_business_evidence.png) | Completed |
| 11 | [Participant-Safe Parkinson's Voice Classification](projects/11-parkinsons-disease-detection/) | Grouped biomedical classification | Zero participant overlap; eight-person holdout balanced accuracy `0.750`, sensitivity `1.000`, specificity `0.500`. | [Notebook](projects/11-parkinsons-disease-detection/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/11-parkinsons-disease-detection/reports/figures/participant_safe_model_evidence.png) | Completed |
| 12 | [Online Retail Customer Segmentation](projects/12-online-retail-segmentation/) | RFM clustering and stability analysis | 4,338 customers segmented into two stable groups; silhouette `0.432`, seed ARI `0.999`. | [Notebook](projects/12-online-retail-segmentation/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/12-online-retail-segmentation/reports/figures/online_retail_segmentation_evidence.png) | Completed |
| 13 | [Historical COVID-19 Next-Day Case Modeling](projects/13-covid-outbreak-prediction/) | Historical panel forecasting | Seven-day rolling baseline remains strongest; final RMSE `388.2`, R² `0.964`, diagnostic interval coverage `89.6%`. | [Notebook](projects/13-covid-outbreak-prediction/notebooks/01_end_to_end_analysis.ipynb) · [Figure](projects/13-covid-outbreak-prediction/reports/figures/historical_covid_validation_evidence.png) | Completed |

---

## Portfolio at a Glance

| Coverage area | Demonstrated through |
|---|---|
| Statistical inference | Projects 01 and 03 |
| Robust and non-parametric alternatives | Projects 01 and 03 |
| Decision-oriented EDA | Projects 01, 02, and 10 |
| Principal component analysis | Project 03 |
| Mixed-type ML pipelines | Projects 04, 06, and 07 |
| Regression and uncertainty | Project 05 |
| Calibration and threshold analysis | Projects 04, 06, and 07 |
| Natural language processing | Project 08 |
| Rolling-origin forecasting | Projects 09 and 13 |
| Basket and retail analytics | Project 10 |
| Grouped participant validation | Project 11 |
| RFM segmentation and cluster stability | Project 12 |
| Explainability and error analysis | Projects 04–07, 11, and 13 |
| Reproducible artifacts and CI | All 13 projects |

---

## Selected Results

The repository README intentionally surfaces a small set of representative results. Complete charts, diagnostic tables, assumptions, and conclusions remain inside the individual projects.

| Insurance claim modeling | Cubic zirconia price modeling |
|---|---|
| [![Insurance model evidence](projects/04-insurance-claim-prediction/reports/figures/insurance_model_evidence.png)](projects/04-insurance-claim-prediction/notebooks/01_end_to_end_analysis.ipynb) | [![Gem-price evidence](projects/05-gem-price-regression/reports/figures/gem_price_model_evidence.png)](projects/05-gem-price-regression/notebooks/01_end_to_end_analysis.ipynb) |
| **Tuned random forest** · ROC-AUC 0.800 · PR-AUC 0.618 | **Histogram gradient boosting** · R² 0.981 · RMSE 562.0 |

| Wine sales forecasting | Online Retail segmentation |
|---|---|
| [![Wine forecasting evidence](projects/09-wine-sales-forecasting/reports/figures/wine_forecasting_evidence.png)](projects/09-wine-sales-forecasting/notebooks/01_end_to_end_analysis.ipynb) | [![Online Retail segmentation](projects/12-online-retail-segmentation/reports/figures/online_retail_segmentation_evidence.png)](projects/12-online-retail-segmentation/notebooks/01_end_to_end_analysis.ipynb) |
| **Rolling-origin selection** · Rose RMSE 13.6 · Sparkling R² 0.932 | **Stable RFM solution** · 4,338 customers · silhouette 0.432 · seed ARI 0.999 |

---

## What the Portfolio Covers

### Statistical Decision-Making and Dimensionality Reduction

- **Statistical Methods for Decision-Making** combines descriptive statistics, confidence intervals, robust tests, effect sizes, multiple-testing correction, and practical specification decisions.
- **Salary ANOVA and College Admissions PCA** compares classic, Welch, and rank-based inference before using standardized PCA for interpretable dimensionality reduction.

These projects demonstrate assumption checking, inferential robustness, practical significance, interaction analysis, loading interpretation, and careful communication of limited observational samples.

### Classification and Propensity Modeling

- **Insurance Claim Propensity** evaluates logistic regression, decision trees, random forests, gradient boosting, and neural networks under class imbalance.
- **Holiday Package Propensity** emphasizes calibration, threshold trade-offs, and campaign decision costs.
- **Election Survey Classification** demonstrates historical respondent-level classification while explicitly avoiding live polling claims.
- **Parkinson's Voice Classification** uses participant-grouped validation so recordings from the same person cannot appear in training and test data.

These projects demonstrate preprocessing inside folds, cross-validation, baselines, calibration, ROC-AUC, PR-AUC, sensitivity, specificity, balanced accuracy, threshold selection, permutation importance, subgroup review, and responsible model governance.

### Regression and Forecasting

- **Cubic Zirconia Price Modeling** compares linear and nonlinear models, diagnoses residuals, evaluates segment-level errors, and estimates an empirical uncertainty band.
- **Wine Sales Forecasting** uses rolling-origin model selection and untouched chronological holdouts for two monthly product series.
- **Historical COVID-19 Modeling** compares lag-only models against simple forecasting baselines while preserving temporal order.

These projects demonstrate baseline discipline, chronological validation, RMSE, MAE, R², MAPE, interval coverage, residual review, and the value of retaining simple models when they outperform more complex alternatives.

### Customer, Marketing, and Retail Analytics

- **Uber Drive Analysis** repairs mixed-format timestamps and converts trip logs into route, purpose, weekday, mileage, and outlier evidence.
- **Cafe Marketing and Retail Analytics** combines revenue analysis, daypart patterns, basket-pair lift, and menu-item segmentation.
- **Online Retail Customer Segmentation** builds customer-level RFM features and evaluates K-means and Gaussian mixture candidates with internal metrics, seed stability, and outlier sensitivity.

These projects demonstrate data cleaning, KPI development, customer-level feature engineering, association measures, cluster profiling, segmentation stability, and experiment-oriented recommendations.

### Natural Language Processing

- **Presidential Speech Analysis** evaluates three inaugural addresses using lexical metrics, readability, TF-IDF terms, cosine similarity, n-grams, and exploratory topic modeling.

The project deliberately treats a three-document corpus as exploratory evidence, not as a basis for broad historical or political conclusions.

---

## Project Summaries

### 01 — Statistical Methods for Decision-Making

[![Open Project 01](https://img.shields.io/badge/Open-Project%2001-2ea44f.svg)](projects/01-statistical-methods/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/01-statistical-methods/notebooks/01_end_to_end_analysis.ipynb)

This project connects wholesale-customer behavior, survey association, and manufacturing specification questions to appropriate statistical methods.

**Key capabilities:** descriptive analysis; coefficient of variation; Welch and Mann–Whitney tests; Holm correction; Cohen's d; chi-square and Cramér's V; confidence intervals; one-sample t and Wilcoxon tests.

**Verified finding:** Shingle B provides evidence of mean moisture below 0.35 (`p=0.0021`), while Shingle A does not meet the prespecified one-sided t-test threshold (`p=0.0748`).

---

### 02 — Uber Drive Behavior and Productivity Analysis

[![Open Project 02](https://img.shields.io/badge/Open-Project%2002-2ea44f.svg)](projects/02-uber-drive-analysis/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/02-uber-drive-analysis/notebooks/01_end_to_end_analysis.ipynb)

This project repairs mixed-format trip timestamps and analyzes mileage, duration, purpose completeness, recurring routes, temporal concentration, and anomalous trips.

**Key capabilities:** datetime repair; quality funnel; KPI engineering; route aggregation; temporal analysis; speed and distance checks; privacy-aware recommendations.

**Verified finding:** 1,154 valid trips cover 12,194.8 miles, with Friday leading weekday mileage and Meeting leading known-purpose mileage.

---

### 03 — Salary Factor Analysis and College Admissions PCA

[![Open Project 03](https://img.shields.io/badge/Open-Project%2003-2ea44f.svg)](projects/03-anova-pca-analysis/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/03-anova-pca-analysis/notebooks/01_end_to_end_analysis.ipynb)

This project evaluates salary differences across education and occupation, tests interaction structure, and reduces 17 standardized college indicators with PCA.

**Key capabilities:** classic and Welch ANOVA; Kruskal–Wallis; Levene testing; eta-squared; Holm-adjusted comparisons; interaction analysis; PCA loadings; explained variance; reconstruction error.

**Verified finding:** education has a large observed association with salary (`eta²=0.626`), while six principal components retain at least 80% of standardized college-indicator variance.

---

### 04 — Insurance Claim Propensity Modeling

[![Open Project 04](https://img.shields.io/badge/Open-Project%2004-2ea44f.svg)](projects/04-insurance-claim-prediction/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/04-insurance-claim-prediction/notebooks/01_end_to_end_analysis.ipynb)

This project compares six classification approaches, tunes the strongest candidate using training-only search, and evaluates discrimination, calibration, threshold behavior, and permutation importance.

**Key capabilities:** imbalanced classification; mixed numeric/categorical preprocessing; stratified CV; randomized search; PR-AUC selection; calibration; threshold analysis; explainability.

**Verified finding:** the tuned random forest reaches test ROC-AUC `0.800`, PR-AUC `0.618`, and balanced accuracy `0.709`.

---

### 05 — Cubic Zirconia Price Modeling

[![Open Project 05](https://img.shields.io/badge/Open-Project%2005-2ea44f.svg)](projects/05-gem-price-regression/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/05-gem-price-regression/notebooks/01_end_to_end_analysis.ipynb)

This project compares median, linear, regularized, random-forest, and histogram-gradient-boosting regressors using training-only cross-validation and an untouched test set.

**Key capabilities:** regression pipelines; missing-data handling; nonlinear modeling; residual diagnostics; segment-level error; permutation importance; empirical prediction intervals.

**Verified finding:** histogram gradient boosting reaches test R² `0.981` and RMSE `562.0`; the training-calibrated diagnostic interval covers `90.7%` of test outcomes.

---

### 06 — Holiday Package Purchase Propensity

[![Open Project 06](https://img.shields.io/badge/Open-Project%2006-2ea44f.svg)](projects/06-holiday-package-prediction/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/06-holiday-package-prediction/notebooks/01_end_to_end_analysis.ipynb)

This project predicts package purchase propensity and demonstrates why probability calibration and operating-threshold selection matter for campaign decisions.

**Key capabilities:** baseline comparison; cross-validation; probability calibration; out-of-fold threshold selection; precision-recall trade-offs; business interpretation.

**Verified finding:** calibrated logistic regression reaches test ROC-AUC `0.730` and PR-AUC `0.707`; a high-recall threshold achieves `93.0%` recall but only `18.6%` specificity.

---

### 07 — Retrospective Election Survey Classification

[![Open Project 07](https://img.shields.io/badge/Open-Project%2007-2ea44f.svg)](projects/07-election-exit-poll-prediction/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/07-election-exit-poll-prediction/notebooks/01_end_to_end_analysis.ipynb)

This historical project compares respondent-classification models and distinguishes retrospective classification from representative polling or election forecasting.

**Key capabilities:** candidate comparison; stratified CV; calibration; ROC and PR evaluation; subgroup sensitivity; permutation importance; political-model limitations.

**Verified finding:** the calibrated random forest reaches test ROC-AUC `0.907`, PR-AUC `0.951`, and balanced accuracy `0.800`.

---

### 08 — U.S. Presidential Inaugural Speech Analysis

[![Open Project 08](https://img.shields.io/badge/Open-Project%2008-2ea44f.svg)](projects/08-presidential-speech-analysis/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/08-presidential-speech-analysis/notebooks/01_end_to_end_analysis.ipynb)

This project compares the Roosevelt 1941, Kennedy 1961, and Nixon 1973 inaugural addresses with interpretable text analytics.

**Key capabilities:** text normalization; lexical diversity; readability; unigram/bigram TF-IDF; distinctive terms; cosine similarity; sentence-level NMF topics.

**Verified finding:** Kennedy and Nixon form the most similar tested pair, but the low cosine score (`0.114`) and three-speech corpus require cautious interpretation.

---

### 09 — Wine Sales Forecasting with Rolling-Origin Validation

[![Open Project 09](https://img.shields.io/badge/Open-Project%2009-2ea44f.svg)](projects/09-wine-sales-forecasting/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/09-wine-sales-forecasting/notebooks/01_end_to_end_analysis.ipynb)

This project compares seasonal naïve, trend-plus-month, additive Holt–Winters, and lag-based ridge forecasts using three rolling-origin windows and an untouched 24-month holdout.

**Key capabilities:** chronological splitting; seasonal baselines; rolling-origin validation; smoothing; lag regression; forecast intervals; residual autocorrelation review.

**Verified finding:** trend plus month is selected for Rose (holdout RMSE `13.6`); additive Holt–Winters is selected for Sparkling (RMSE `358.7`, R² `0.932`).

---

### 10 — Cafe Marketing and Retail Analytics

[![Open Project 10](https://img.shields.io/badge/Open-Project%2010-2ea44f.svg)](projects/10-marketing-retail-analysis/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/10-marketing-retail-analysis/notebooks/01_end_to_end_analysis.ipynb)

This project turns line-item transactions into revenue, order, daypart, basket-pair, and menu-segmentation evidence.

**Key capabilities:** transaction cleaning; revenue KPIs; average order value; daypart analysis; pair support, confidence, and lift; item clustering; operational recommendations.

**Verified finding:** the cleaned year contains 69,982 bills and 32.65M recorded revenue units; two menu groups achieve silhouette `0.395`.

---

### 11 — Participant-Safe Parkinson's Voice Classification

[![Open Project 11](https://img.shields.io/badge/Open-Project%2011-2ea44f.svg)](projects/11-parkinsons-disease-detection/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/11-parkinsons-disease-detection/notebooks/01_end_to_end_analysis.ipynb)

This project derives participant identifiers from recording names and evaluates models at participant level so one person's recordings cannot leak across data splits.

**Key capabilities:** grouped splitting; StratifiedGroupKFold; participant aggregation; bootstrap intervals; false-negative review; permutation importance; clinical-use boundaries.

**Verified finding:** the holdout has eight participants and zero overlap with training; balanced accuracy is `0.750`, with sensitivity `1.000` and specificity `0.500`. The sample is too small for clinical use.

---

### 12 — Online Retail Customer Segmentation

[![Open Project 12](https://img.shields.io/badge/Open-Project%2012-2ea44f.svg)](projects/12-online-retail-segmentation/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/12-online-retail-segmentation/notebooks/01_end_to_end_analysis.ipynb)

This project cleans the verified UCI Online Retail transactions, engineers customer-level RFM behavior, and compares K-means with Gaussian mixture candidates.

**Key capabilities:** cancellation and duplicate handling; RFM engineering; log transformation; K-means and GMM; silhouette, Davies–Bouldin, and Calinski–Harabasz metrics; seed stability; outlier sensitivity; segment profiles.

**Verified finding:** 4,338 customers form two stable behavioral groups with silhouette `0.432`, seed ARI `0.999`, and outlier-sensitivity ARI `0.985`.

---

### 13 — Historical COVID-19 Next-Day Case Modeling

[![Open Project 13](https://img.shields.io/badge/Open-Project%2013-2ea44f.svg)](projects/13-covid-outbreak-prediction/)
[![Executed Notebook](https://img.shields.io/badge/Jupyter-Executed%20Notebook-F37626.svg)](projects/13-covid-outbreak-prediction/notebooks/01_end_to_end_analysis.ipynb)

This project constructs leakage-safe lag features for historical country-day data and compares simple baselines with ridge and gradient-boosting alternatives under rolling temporal validation.

**Key capabilities:** panel cleaning; lag-only features; rolling-origin windows; baseline comparison; final chronological holdout; country-level errors; diagnostic interval coverage.

**Verified finding:** the seven-day rolling baseline outperforms the tested learned models; final historical holdout RMSE is `388.2`, R² is `0.964`, and diagnostic interval coverage is `89.6%`.

---

## Evaluation Coverage

The projects use evaluation methods aligned with each problem rather than applying one metric universally.

| Task | Evaluation methods |
|---|---|
| Statistical inference | Confidence intervals, p-values, effect sizes, robust alternatives, assumption checks, Holm correction |
| Binary classification | ROC-AUC, PR-AUC, balanced accuracy, precision, recall, specificity, F1, Brier score, calibration |
| Regression | RMSE, MAE, R², MAPE, residual diagnostics, segment error, empirical interval coverage |
| Forecasting | Rolling-origin RMSE/MAE/MAPE, final chronological holdout, interval coverage, residual autocorrelation |
| Clustering | Silhouette, Davies–Bouldin, Calinski–Harabasz, seed ARI, outlier-sensitivity ARI, profile coherence |
| PCA | Explained variance, loadings, retained-component thresholds, reconstruction error |
| NLP | Corpus metrics, readability, distinctive TF-IDF terms, cosine similarity, topic shares |
| Retail analytics | Revenue, order value, support, confidence, lift, temporal concentration, segment profiles |

### Why multiple evaluation methods matter

- Accuracy alone can hide minority-class failures.
- ROC-AUC can appear strong when operational precision remains modest.
- A low RMSE does not guarantee uniform performance across value segments.
- Forecast models must be assessed on future periods, not random splits.
- Repeated patient recordings require grouped evaluation.
- A high silhouette score does not make clusters objectively true customer types.
- Statistical significance does not automatically imply practical importance.
- Model complexity is not evidence of value; a validated baseline may be the correct final model.

---

## What the Repository Demonstrates

### End-to-End Analytical Delivery

- problem framing and decision definition;
- data acquisition, schema review, and provenance documentation;
- reproducible cleaning and feature engineering;
- exploratory and inferential analysis;
- appropriate train/validation/test design;
- baseline and candidate development;
- tuning without test-set leakage;
- evaluation, diagnostics, and sensitivity analysis;
- saved models, metrics, tables, and figures;
- executed notebook evidence;
- concise stakeholder conclusions;
- documented limitations and responsible-use boundaries.

### Model Selection Based on Evidence

The repository does not assume that the newest or most complex model is automatically best. Examples include:

- a tuned random forest selected by training PR-AUC for insurance ranking;
- histogram gradient boosting materially outperforming linear gem-price models;
- calibrated logistic regression retained for interpretable holiday propensity;
- a simple seven-day rolling baseline outperforming learned COVID-19 candidates;
- separate Rose and Sparkling forecast models selected under identical rolling-origin rules;
- a compact two-segment Online Retail solution favored for stability and minimum segment size;
- honest retention of modest, uncertain, or negative results.

### Reliable and Reusable Engineering

- modular `src/analysis.py` entry points;
- shared metric and reporting utilities in `portfolio_lib/`;
- project-relative paths instead of machine-specific locations;
- deterministic random seeds;
- preprocessing contained inside model pipelines;
- machine-readable `metrics.json` outputs;
- saved CSV evidence tables and PNG figures;
- serialized models where reuse is meaningful;
- executed notebooks with persisted outputs;
- repository-wide validation and automated tests;
- GitHub Actions validation on Python 3.12 and 3.13;
- `.gitignore` protection for virtual environments, caches, logs, and temporary artifacts.

### Responsible Analytical Communication

The projects avoid presenting portfolio analyses as:

- automatic medical diagnostic systems;
- insurance approval, denial, pricing, or investigation systems;
- live election forecasts;
- current pandemic forecasts or policy tools;
- discriminatory customer-pricing systems;
- universal conclusions beyond the evaluated samples.

Weaknesses, rejected models, uncertain estimates, historical limitations, and missing business-cost information are retained where they improve technical honesty.

---

## Repository Convention

The repository is organized as a reproducible monorepo:

```text
applied-data-science-machine-learning-portfolio/
├── .github/
│   └── workflows/
│       └── quality.yml
├── docs/
│   └── ARCHITECTURE.md
├── execution_logs/
│   └── latest_run_summary.json
├── portfolio_lib/
│   ├── modeling.py
│   └── reporting.py
├── projects/
│   ├── 01-statistical-methods/
│   ├── 02-uber-drive-analysis/
│   ├── 03-anova-pca-analysis/
│   ├── 04-insurance-claim-prediction/
│   ├── 05-gem-price-regression/
│   ├── 06-holiday-package-prediction/
│   ├── 07-election-exit-poll-prediction/
│   ├── 08-presidential-speech-analysis/
│   ├── 09-wine-sales-forecasting/
│   ├── 10-marketing-retail-analysis/
│   ├── 11-parkinsons-disease-detection/
│   ├── 12-online-retail-segmentation/
│   └── 13-covid-outbreak-prediction/
├── scripts/
├── tests/
├── README.md
├── MODEL_RESULTS_SUMMARY.md
├── PORTFOLIO_AUDIT.md
├── PROJECT_STATUS_MATRIX.md
├── REPRODUCIBILITY_REPORT.md
├── RUN_INSTRUCTIONS.md
├── run_all.py
└── validate_portfolio.py
```

Each project follows a consistent pattern:

```text
project-folder/
├── data/
│   ├── source dataset files
│   └── README.md
├── models/
│   └── fitted artifact where appropriate
├── notebooks/
│   └── 01_end_to_end_analysis.ipynb
├── reports/
│   ├── figures/
│   ├── tables/
│   └── metrics.json
├── src/
│   └── analysis.py
├── PROJECT_SUMMARY.md
└── README.md
```

---

## Continuous Integration

The repository uses one focused portfolio workflow with a Python-version matrix.

For both Python 3.12 and 3.13, CI checks:

- dependency installation;
- supported scientific-library imports;
- exact 13-project structure;
- Python source syntax;
- required project entry points;
- metrics status;
- saved evidence tables and figures;
- notebook size and code-cell count;
- execution counts and saved outputs;
- absence of notebook error outputs;
- Markdown link integrity;
- nested Git repositories;
- machine-specific paths and secret-like strings;
- automated evaluation contracts.

[![Open GitHub Actions](https://img.shields.io/badge/Open-GitHub%20Actions-2088ff?style=for-the-badge)](https://github.com/unit-mole/applied-data-science-machine-learning-portfolio/actions)

---

## Run the Portfolio Locally

### 1. Clone the repository

```bash
git clone https://github.com/unit-mole/applied-data-science-machine-learning-portfolio.git
cd applied-data-science-machine-learning-portfolio
```

### 2. Windows automated setup and full execution

From Command Prompt:

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\setup_and_run.ps1"
```

This creates `.venv`, installs the dependencies, executes all 13 pipelines, regenerates and executes all notebooks, builds the portfolio reports, validates the repository, and runs the automated tests.

### 3. Manual Python 3.12 or 3.13 setup

**Windows**

```cmd
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[notebooks,dev]"
.venv\Scripts\python.exe run_all.py
```

Use `py -3.13` instead when Python 3.13 is preferred.

**macOS or Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[notebooks,dev]'
python run_all.py
```

### 4. Validate without retraining

```cmd
.venv\Scripts\python.exe validate_portfolio.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### 5. Run one project

```cmd
.venv\Scripts\python.exe projects\04-insurance-claim-prediction\src\analysis.py
```

Detailed alternatives are provided in [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md).

---

## Results and Reproducibility Directory

| Resource | Purpose |
|---|---|
| [Portfolio Audit](PORTFOLIO_AUDIT.md) | Original-state findings, provenance decisions, and rebuild scope |
| [Project Status Matrix](PROJECT_STATUS_MATRIX.md) | Completion, validation, results, and known limitations for all 13 projects |
| [Model Results Summary](MODEL_RESULTS_SUMMARY.md) | Candidate comparisons and final analytical results |
| [Reproducibility Report](REPRODUCIBILITY_REPORT.md) | Runtime, package versions, notebook execution, hashes, and acceptance evidence |
| [Run Instructions](RUN_INSTRUCTIONS.md) | Detailed Windows, macOS, and Linux commands |
| [Delivery Report](DELIVERY_REPORT.md) | Delivered artifacts and acceptance criteria |
| [Changelog](CHANGELOG.md) | Changes introduced by the portfolio rebuild |

All headline numerical claims in this README are grounded in executed `reports/metrics.json` artifacts.

---

## Responsible Use

This repository is intended for education, experimentation, technical demonstration, and portfolio presentation.

General limitations include:

- classroom datasets may lack complete sampling or redistribution documentation;
- historical samples do not establish present-day model performance;
- observational relationships do not establish causality;
- holdout metrics remain estimates and may vary under distribution shift;
- cluster labels summarize behavior but are not objective customer identities;
- probability estimates require current calibration before operational use;
- empirical uncertainty bands are not universal guarantees;
- small biomedical holdouts produce wide uncertainty;
- political and public-health datasets require especially careful communication;
- portfolio models are not automatically production-ready;
- no analysis should be the sole basis for a safety-critical, clinical, financial, insurance, employment, or policy decision.

Important decisions require current data, domain expertise, fairness review, external validation, monitoring, and human accountability.

---

## Technical Coverage

| Area | Demonstrated through |
|---|---|
| Descriptive and inferential statistics | Projects 01 and 03 |
| Confidence intervals and effect sizes | Projects 01 and 03 |
| Multiple-testing correction | Projects 01 and 03 |
| Principal component analysis | Project 03 |
| Logistic regression | Projects 04, 06, and 07 |
| Decision trees and random forests | Projects 04 and 07 |
| Gradient boosting | Projects 04, 05, 11, and 13 |
| Neural-network comparison | Project 04 |
| Probability calibration | Projects 04, 06, and 07 |
| Threshold optimization | Projects 04 and 06 |
| Regression diagnostics | Project 05 |
| TF-IDF and text similarity | Project 08 |
| Topic modeling | Project 08 |
| Time-series forecasting | Projects 09 and 13 |
| Basket-pair analysis | Project 10 |
| Grouped biomedical evaluation | Project 11 |
| K-means and Gaussian mixture clustering | Project 12 |
| Cluster stability and sensitivity | Projects 10 and 12 |
| Permutation importance | Projects 04–07 and 11 |
| Reproducible notebook execution | All 13 projects |
| GitHub Actions and automated validation | Entire portfolio |

---

## Core Skills Demonstrated

`Python` · `NumPy` · `pandas` · `SciPy` · `scikit-learn` · `Matplotlib` · `Jupyter` · `Statistical Inference` · `Hypothesis Testing` · `Confidence Intervals` · `Effect Sizes` · `ANOVA` · `Welch ANOVA` · `Non-Parametric Testing` · `Multiple-Testing Correction` · `PCA` · `Exploratory Data Analysis` · `Feature Engineering` · `Regression` · `Classification` · `Random Forests` · `Gradient Boosting` · `Neural Networks` · `Cross-Validation` · `Grouped Validation` · `Chronological Validation` · `Probability Calibration` · `Threshold Analysis` · `ROC-AUC` · `PR-AUC` · `Residual Diagnostics` · `Forecasting` · `Natural Language Processing` · `TF-IDF` · `Topic Modeling` · `Customer Segmentation` · `RFM Analysis` · `K-Means` · `Gaussian Mixtures` · `Basket Analysis` · `Permutation Importance` · `Model Governance` · `Testing` · `GitHub Actions` · `CI/CD` · `Responsible Data Science Communication`

---

## Portfolio Positioning

**One-line description:** Thirteen fully executed end-to-end data science and machine learning projects spanning statistics, regression, classification, PCA, NLP, forecasting, retail analytics, grouped biomedical evaluation, and customer segmentation.

**Pinned repository description:** Professional applied data science portfolio featuring 13 executed projects with verified datasets, leakage-safe evaluation, saved notebook outputs, model comparisons, explainability, business conclusions, reproducible Python 3.12/3.13 pipelines, and automated GitHub Actions validation.

This portfolio connects directly to a Quality Data Scientist background because the demonstrated methods support:

- product and process quality analysis;
- specification and hypothesis testing;
- customer and field-performance analytics;
- defect or claim propensity modeling;
- pricing and forecasting decisions;
- operational KPI development;
- transactional and retail analysis;
- segmentation and prioritization;
- evidence-based model comparison;
- reproducible analytical reporting;
- validation, release governance, and responsible communication.

---

## License

This repository is distributed under the [MIT License](LICENSE).

Individual datasets, models, and third-party libraries remain subject to their original licenses, source terms, and usage conditions. Dataset-specific provenance and limitations are documented inside each project's `data/README.md`.

---

## Author

**Anmol Tripathi**  
Quality Data Scientist | Data Science | Machine Learning | Applied AI | Statistical Analysis | Predictive Analytics | Analytics Engineering | Quality Analytics

[![GitHub](https://img.shields.io/badge/GitHub-unit--mole-181717.svg?logo=github)](https://github.com/unit-mole)
