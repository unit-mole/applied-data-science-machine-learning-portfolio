# Portfolio Audit

## Scope and decision

This rebuild covers the 13 projects named in the master brief. The uploaded `Project - Data Mining Clustering(1).ipynb` is retained as source evidence but is not promoted as a fourteenth project: its 210-row, seven-variable structure matches the previously identified seed-measurement provenance problem rather than verified bank-customer data. Customer clustering is represented by the documented UCI Online Retail transaction project.

The original notebooks are preserved in the conversation uploads and source repositories. Work below is performed in the separate `applied-data-science-portfolio-rebuilt/` directory.

## Cross-portfolio findings

- The originals contain substantial exploratory work (15–355 code cells), but most are structured as classroom question-and-answer notebooks rather than stakeholder-facing analytical products.
- `Machine Learning Problem 1(1).ipynb` contains a saved `SyntaxError`; `Time Series Forecasting(1).ipynb` contains a saved `KeyError`.
- The Parkinson notebook contains a hard-coded personal Windows path and risks patient leakage if recordings are split randomly.
- Most predictive notebooks compare models on a single split without a separate model-selection process, calibrated probabilities, uncertainty, threshold analysis, or reproducible pipelines.
- The time-series notebooks require stricter chronological validation and multiple forecast origins.
- Dataset provenance is incomplete for several classroom datasets. Those limitations must remain explicit and cannot be repaired by inventing a source.
- Existing conclusions and reported metrics are treated as unverified until reproduced by the rebuilt code.

## Project audit

| Project | Original objective and available source | Dataset status | Strengths worth retaining | Primary weaknesses / leakage risk | Rebuild decision | Priority |
|---|---|---|---|---|---|---|
| 01 Statistical Methods | `Module 2 - SMDM Assignment(1).ipynb`; wholesale, survey, and shingles CSV files | Available; wholesale provenance identifiable; survey and shingles provenance unclear | Multiple business questions, descriptive statistics, hypothesis tests | Assumptions, effect sizes, confidence intervals, multiplicity, and practical significance are incomplete; leakage not applicable | Add formal data-quality audit, assumption checks, effect sizes, Holm correction, robust alternatives, confidence intervals, and decision interpretation | High |
| 02 Uber Drive Analysis | `PDS_UberDriveProject_Solutions(1).ipynb`; personal trip CSV | Available; upstream collection and license unclear | Thorough introductory inspection and cleaning questions | Assignment-style sequence, limited temporal insight, missing-purpose treatment not decision-oriented; leakage not applicable | Build a rigorous EDA case study with trip-duration checks, day/time behavior, route concentration, outliers, and operational recommendations | Medium |
| 03 Salary ANOVA and Admissions PCA | Two uploaded advanced-statistics notebooks; salary and college data | Available; college source identifiable; salary provenance unclear | Correct separation of ANOVA and PCA questions | Very small salary sample, limited robust alternatives/post-hoc evidence, weak loading interpretation; leakage low | Add factorial diagnostics, Welch/Kruskal sensitivity, corrected pairwise comparisons, effect sizes, PCA stability/loadings, and information-loss analysis | High |
| 04 Insurance Claim Prediction | `Project - Data Mining CART-RF-ANN(1).ipynb`; insurance CSV | Available; 139 exact duplicates; upstream provenance unclear | Rich EDA and several classifier families | Model selection and final evaluation are not cleanly separated; imbalance, calibration, thresholds, and explainability are weak; leakage medium | Use train-only CV, dummy baseline, tuned candidates, untouched test set, calibration, threshold analysis, permutation importance, and error analysis | Critical |
| 05 Gem Price Regression | `Predictive Modelling Question 1(1).ipynb`; cubic-zirconia CSV | Available; source license unclear; identifier column and missing values present | Extensive EDA and linear-regression foundation | Linear-only framing, limited nonlinear comparison, heteroscedasticity and uncertainty not resolved; leakage medium if preprocessing precedes split | Compare linear, regularized/log-target, and nonlinear pipelines with CV, residual diagnostics, segment errors, and conformal-style interval evidence | Critical |
| 06 Holiday Package Prediction | `Predictive Modelling Question 2(1).ipynb`; package CSV | Available; upstream provenance unclear | Customer profiling and interpretable classification | Small sample, single-split dependence, limited calibration and campaign-threshold reasoning; leakage medium | Use stratified CV, baseline and ensemble comparison, calibration, threshold table, permutation importance, and targeted but non-causal recommendations | High |
| 07 Election Survey Classification | `Machine Learning Problem 1(1).ipynb`; election workbook | Available; sampling/weighting provenance unclear | Broad EDA and multiple model families | Saved `SyntaxError`; historical classroom sample cannot support live polling claims; single-split sensitivity; leakage medium | Rebuild as retrospective classification with CV, calibration, subgroup sensitivity, uncertainty, and strict political-use limitations | Critical |
| 08 Presidential Speech Analysis | `Machine Learning Problem 2(1).ipynb`; three speech workbooks | Available; NLTK inaugural-corpus lineage documented | Transparent text cleaning and frequency analysis | Only three documents, limited reproducible NLP evaluation, automated interpretation can be overstated; leakage low | Add corpus audit, lexical diversity/readability, unigram/bigram TF–IDF, similarity, sentence-level exploratory topics, and explicit interpretive caveats | Medium |
| 09 Wine Sales Forecasting | `Time Series Forecasting(1).ipynb`; Rose and Sparkling CSVs | Available; two missing Rose observations; commercial units/source unclear | Very extensive decomposition and forecasting experimentation | Saved `KeyError`; very large notebook; selection and evaluation windows are mixed; leakage high if future holdout informs tuning | Use final chronological holdout plus rolling-origin selection, seasonal-naive baseline, ETS and lag models, intervals, and residual diagnostics | Critical |
| 10 Marketing and Retail Analysis | `MRA Project(1).ipynb`; cafe transactions workbook | Available; 680 exact duplicates; no customer identifier | Useful transaction summaries and item clustering | Business question is underdeveloped; customer RFM is impossible; limited basket/daypart analysis; leakage low | Focus on revenue, orders, categories, dayparts, basket co-occurrence, and stable menu-item segmentation supported by actual fields | High |
| 11 Parkinson's Disease Detection | `Parkinson's Disease Detection(1).ipynb`; UCI-style voice data | Available; 195 recordings from 32 participants | Multiple classifier families and voice-feature exploration | Hard-coded local paths; random record splits can leak participant identity; high-stakes claims; leakage high | Enforce participant-grouped CV and holdout, report participant-level sensitivity/specificity and uncertainty, analyze false negatives, and state non-clinical scope | Critical |
| 12 Online Retail Segmentation | `Customer_Segmentation(1).ipynb`; UCI Online Retail workbook | Available; missing customer IDs, cancellations, returns, and duplicates require explicit treatment | RFM construction and preliminary segmentation | Cleaning and outlier decisions need sensitivity analysis; cluster selection/stability and labels are weak; leakage low | Build auditable RFM, compare cluster counts and methods, quantify stability and outlier sensitivity, name evidence-supported segments, and link actions to profiles | Critical |
| 13 Historical COVID Modeling | `covid-19-outbreak-prediction(1).ipynb`; early-pandemic country-date CSV | Available; extensive missingness and revision artifacts; exact snapshot provenance incomplete | Clear introductory workflow | Random or simplified regression is unsuitable for temporal public-health data; uncertainty and baselines are weak; leakage high | Use lag-only features, multiple chronological windows, naive baselines, country-level errors, interval evidence, and strict historical/non-operational framing | Critical |

## Reproducibility assessment before rebuild

| Area | Original status | Rebuild requirement |
|---|---|---|
| Portable paths | Mixed; one notebook contains user-specific paths | `pathlib` and repository-relative paths only |
| Clean execution | Two uploaded notebooks have saved errors | Zero error outputs across all primary notebooks |
| Dependency control | Inconsistent or absent | Python 3.12/3.13 metadata and bounded dependencies |
| Validation | Mostly single split or assignment output | Problem-appropriate CV/grouped/chronological validation |
| Saved evidence | Outputs exist but are not systematically linked | Versioned metrics, tables, figures, models, and execution manifest |
| README accuracy | Incomplete and not tied to generated metrics | README values generated from executed result files |
| Testing | Largely absent | Data/schema, feature, split, metric, notebook, and path tests |
