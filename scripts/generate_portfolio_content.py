"""Generate metric-synchronized project READMEs, summaries, data notes, and notebooks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROJECTS = {
    "01-statistical-methods": {
        "title": "Statistical Methods for Decision-Making", "domain": "Business statistics and quality", "problem": "Statistical inference",
        "objective": "Turn wholesale, student-survey, and shingle measurements into assumption-aware business and quality decisions.",
        "dataset": "440 wholesale customers, 62 survey respondents, and 36 shingle rows across three CSV files.",
        "provenance": "Wholesale data aligns with the UCI Wholesale Customers dataset. Survey and shingle collection protocols and reuse terms were not supplied in the original project.",
        "methods": "Descriptive statistics, coefficients of variation, Welch tests, Mann–Whitney sensitivity, Holm correction, chi-square/Cramér's V, one-sample t and Wilcoxon tests, confidence intervals, and effect sizes.",
        "user": "A wholesale manager, survey analyst, or quality engineer", "decision": "Prioritize category/channel investigation and decide whether moisture evidence supports a specification claim.",
        "primary_table": "wholesale_channel_tests.csv", "figure": "statistical_decision_evidence.png",
        "original": "https://github.com/unit-mole/Statistical-Methods-for-Decision-Making",
    },
    "02-uber-drive-analysis": {
        "title": "Uber Drive Behavior and Productivity Analysis", "domain": "Transportation and personal productivity", "problem": "Decision-oriented exploratory analysis",
        "objective": "Audit and summarize a personal trip log to expose temporal, purpose, route, and distance patterns without inventing a prediction target.",
        "dataset": "1,155 source rows containing trip timestamps, categories, locations, distance, and purpose.",
        "provenance": "The dataset is bundled in the original repository; upstream collection context and reuse terms are not documented.",
        "methods": "Mixed-format datetime repair, data-quality rules, duration and speed checks, temporal aggregation, route concentration, missing-purpose analysis, and IQR outlier review.",
        "user": "A traveler, fleet analyst, or expense-process owner", "decision": "Improve purpose capture, route scheduling, mileage review, and reimbursement evidence.",
        "primary_table": "monthly_trip_summary.csv", "figure": "uber_trip_behavior_evidence.png",
        "original": "https://github.com/unit-mole/Python-for-Data-Science-on-Uber-Drive-",
    },
    "03-anova-pca-analysis": {
        "title": "Salary Factor Analysis and College Admissions PCA", "domain": "Compensation and higher education", "problem": "Factorial inference and dimensionality reduction",
        "objective": "Assess salary differences with robust sensitivity checks and compress correlated college indicators without hiding information loss.",
        "dataset": "40 salary observations and 777 colleges with 17 numeric admissions and institutional indicators.",
        "provenance": "College data corresponds to the ISLR College dataset; the small salary dataset's sampling process and license are not documented.",
        "methods": "Classic and Welch ANOVA, Kruskal sensitivity, Levene test, eta-squared, Holm-corrected pairwise Welch tests, interaction F-test, standardized PCA, loading interpretation, and reconstruction error.",
        "user": "A compensation analyst or higher-education analyst", "decision": "Identify material group differences and select a defensible reduced indicator set.",
        "primary_table": "salary_pairwise_holm.csv", "figure": "anova_pca_evidence.png",
        "original": "https://github.com/unit-mole/Salary-Analysis-using-ANOVA-and-Principal-Component-Analysis-on-College-Admissions-Data",
    },
    "04-insurance-claim-prediction": {
        "title": "Insurance Claim Propensity Modeling", "domain": "Travel insurance", "problem": "Imbalanced binary classification",
        "objective": "Compare and calibrate claim-propensity models using training-only selection and an untouched test set.",
        "dataset": "3,000 policy rows with demographic, agency, product, destination, duration, sales, commission, channel, and claim fields.",
        "provenance": "Bundled in the original repository; the upstream sampling frame, collection process, and redistribution terms are not documented.",
        "methods": "Duplicate leakage control, mixed-type pipelines, dummy baseline, logistic/CART/random-forest/boosting/MLP comparison, randomized tuning, stratified CV, calibration, threshold selection, PR-AUC, and permutation importance.",
        "user": "An insurance analytics or operations team", "decision": "Understand ranking and threshold trade-offs while keeping claim decisions under human governance.",
        "primary_table": "model_comparison.csv", "figure": "insurance_model_evidence.png",
        "original": "https://github.com/unit-mole/Claim-Status-of-Insurance-firm-using-CART-RF-ANN",
    },
    "05-gem-price-regression": {
        "title": "Cubic Zirconia Price Modeling", "domain": "Retail pricing and appraisal analytics", "problem": "Supervised regression",
        "objective": "Compare interpretable and nonlinear price models, diagnose residual risk, and quantify empirical prediction coverage.",
        "dataset": "26,967 cubic-zirconia records with physical measurements, quality grades, and price.",
        "provenance": "Bundled in the original repository; market period, price units, sampling context, and redistribution terms are not fully documented.",
        "methods": "Leakage-safe imputation/encoding, median baseline, linear and regularized log-target models, random forest, histogram boosting, cross-validation, residual diagnostics, permutation importance, segment errors, and calibration-residual intervals.",
        "user": "A merchandising, pricing, or appraisal analyst", "decision": "Estimate price ranges and identify where prediction errors become operationally material.",
        "primary_table": "model_comparison.csv", "figure": "gem_price_model_evidence.png",
        "original": "https://github.com/unit-mole/Gems-Prediction-using-Linear-Regression",
    },
    "06-holiday-package-prediction": {
        "title": "Holiday Package Purchase Propensity", "domain": "Travel marketing", "problem": "Binary propensity modeling",
        "objective": "Estimate purchase propensity with calibrated probabilities and expose the campaign-volume precision/recall trade-off.",
        "dataset": "872 records with purchase outcome, salary, age, education, children, and foreign-status fields.",
        "provenance": "Bundled in the original repository; collection population, time period, and reuse terms are not documented.",
        "methods": "Stratified CV, prevalence baseline, logistic/LDA/tree/forest/boosting comparison, probability calibration, training-only threshold selection, PR-AUC, ROC-AUC, customer profiling, and permutation importance.",
        "user": "A travel-campaign analyst", "decision": "Choose contact thresholds consistent with capacity and false-positive/false-negative costs.",
        "primary_table": "model_comparison.csv", "figure": "holiday_propensity_evidence.png",
        "original": "https://github.com/unit-mole/Holiday_Package_Prediction",
    },
    "07-election-exit-poll-prediction": {
        "title": "Retrospective Election Survey Classification", "domain": "Political survey research", "problem": "Historical binary classification",
        "objective": "Evaluate respondent-level party classification while explicitly separating it from representative polling or forecasting.",
        "dataset": "1,525 historical survey rows with vote, age, leader ratings, economic assessments, Europe attitudes, knowledge, and gender.",
        "provenance": "Bundled in the original repository; survey organization, weighting, sampling design, and license are undocumented.",
        "methods": "Stratified CV, dummy/logistic/LDA/KNN/SVM/random-forest comparison, probability calibration, untouched test evaluation, permutation importance, and age/gender sensitivity tables.",
        "user": "A survey-methodology analyst", "decision": "Understand classification signal and uncertainty without making live-election claims.",
        "primary_table": "model_comparison.csv", "figure": "election_model_evidence.png",
        "original": "https://github.com/unit-mole/Election_Exit_Poll_Prediction_using_ML_Models",
    },
    "08-presidential-speech-analysis": {
        "title": "U.S. Presidential Inaugural Speech Analysis", "domain": "Natural language processing and political text", "problem": "Small-corpus exploratory NLP",
        "objective": "Compare lexical structure, readability, distinctive terms, similarity, and exploratory topics across three inaugural speeches.",
        "dataset": "The 1941 Roosevelt, 1961 Kennedy, and 1973 Nixon inaugural addresses stored as three workbooks.",
        "provenance": "The original project identifies NLTK's inaugural corpus as the source; local workbooks preserve imported snapshots.",
        "methods": "Corpus-quality audit, tokenization, lexical diversity, approximate Flesch readability, unigram/bigram TF-IDF, cosine similarity, distinctive-term analysis, and sentence-level NMF topics.",
        "user": "A digital-humanities or communications analyst", "decision": "Locate lexical differences for closer human reading rather than automate historical judgment.",
        "primary_table": "distinctive_tfidf_terms.csv", "figure": "speech_analysis_evidence.png",
        "original": "https://github.com/unit-mole/U.S.A_Presidential_Speech_Analysis_using_Machine_Learning",
    },
    "09-wine-sales-forecasting": {
        "title": "Wine Sales Forecasting with Rolling-Origin Validation", "domain": "Retail forecasting", "problem": "Monthly time-series forecasting",
        "objective": "Select transparent monthly forecasting methods on multiple historical origins and evaluate once on a final 24-month holdout.",
        "dataset": "187 monthly Rose and Sparkling observations from January 1980 through July 1995.",
        "provenance": "Bundled in the original repository; commercial source, currency/units, and redistribution terms are not documented.",
        "methods": "Frequency audit, train-contained interpolation, seasonal-naive baseline, trend/month regression, lagged ridge, additive Holt-Winters implementation, three rolling origins, empirical intervals, and Ljung–Box residual autocorrelation.",
        "user": "An inventory or demand-planning analyst", "decision": "Choose a reproducible baseline and quantify forecast risk before inventory commitment.",
        "primary_table": "rolling_origin_results.csv", "figure": "wine_forecasting_evidence.png",
        "original": "https://github.com/unit-mole/Forecasting_Wine_Sales_for_ABC_Estate_Wines_company",
    },
    "10-marketing-retail-analysis": {
        "title": "Cafe Marketing and Retail Analytics", "domain": "Restaurant point-of-sale analytics", "problem": "Transactional business analysis and item segmentation",
        "objective": "Translate point-of-sale lines into revenue, order, daypart, basket, and stable menu-item insights supported by available fields.",
        "dataset": "145,830 cafe line items covering 69,982 bills and one year of activity.",
        "provenance": "Bundled in the original repository; business identity, geography, currency, and redistribution terms are not documented.",
        "methods": "Duplicate control, monthly/category/daypart KPIs, order-value analysis, bill-level pair support/confidence/lift, and stable K-means menu-item segmentation.",
        "user": "A cafe operator or marketing analyst", "decision": "Prioritize menu review, daypart staffing, and carefully tested cross-sell ideas.",
        "primary_table": "basket_item_pairs.csv", "figure": "cafe_business_evidence.png",
        "original": "https://github.com/unit-mole/Marketing_and_Retail_Analysis",
    },
    "11-parkinsons-disease-detection": {
        "title": "Participant-Safe Parkinson's Voice Classification", "domain": "Biomedical machine learning", "problem": "Grouped high-stakes classification",
        "objective": "Evaluate voice-based classification without allowing recordings from one participant to cross train/test boundaries.",
        "dataset": "195 recordings, 22 acoustic features, and 32 derived participant identifiers.",
        "provenance": "Matches the UCI Parkinsons voice dataset; participant IDs are derived from the recording-name field.",
        "methods": "Participant-level holdout, StratifiedGroupKFold selection, dummy/logistic/SVM/forest/boosting comparison, recording and participant metrics, bootstrap intervals, false-negative review, and permutation importance.",
        "user": "A biomedical ML researcher reviewing methodology", "decision": "Judge whether signal warrants external study—not make a clinical decision.",
        "primary_table": "participant_grouped_cv.csv", "figure": "participant_safe_model_evidence.png",
        "original": "https://github.com/unit-mole/Parkinson-s_Disease_Detection_using_ML_Techniques",
    },
    "12-online-retail-segmentation": {
        "title": "Online Retail Customer Segmentation", "domain": "E-commerce customer analytics", "problem": "Unsupervised RFM segmentation",
        "objective": "Create auditable customer profiles after explicit cancellation, return, duplicate, and missing-ID treatment.",
        "dataset": "541,909 UCI Online Retail transaction rows from December 2010 through December 2011.",
        "provenance": "UCI Online Retail dataset; preserve UCI attribution and verify source-specific reuse terms before redistribution.",
        "methods": "Transaction cleaning, customer-level RFM, log scaling, K-means/Gaussian-mixture comparison, silhouette/Davies–Bouldin/Calinski–Harabasz metrics, seed stability, outlier sensitivity, PCA, and evidence-based naming.",
        "user": "An e-commerce CRM or retention analyst", "decision": "Design differentiated retention and reactivation experiments without sensitive profiling.",
        "primary_table": "cluster_model_selection.csv", "figure": "online_retail_segmentation_evidence.png",
        "original": "https://github.com/unit-mole/Customer_segmentaion_online_Retail",
    },
    "13-covid-outbreak-prediction": {
        "title": "Historical COVID-19 Next-Day Case Modeling", "domain": "Public-health time series", "problem": "Historical panel forecasting",
        "objective": "Compare lag-only one-day-ahead models with transparent baselines across multiple chronological windows.",
        "dataset": "19,496 country-date rows from December 2019 through May 2020 with cases, tests, policy, population, and demographic fields.",
        "provenance": "Schema and period align with an early Our World in Data snapshot; exact snapshot checksum and redistribution history were not recorded in the original repository.",
        "methods": "Revision audit, lag/rolling features, three 14-day rolling origins, last-value and rolling baselines, country-aware ridge, histogram boosting, final chronological holdout, diagnostic intervals, and country-level error analysis.",
        "user": "A public-health data scientist reviewing historical methods", "decision": "Assess baseline adequacy and reporting risk—not make a current forecast or policy recommendation.",
        "primary_table": "model_comparison.csv", "figure": "historical_covid_validation_evidence.png",
        "original": "https://github.com/unit-mole/Covid-19-outbreak-prediction",
    },
}


def result_summary(slug: str, metrics: dict[str, object]) -> str:
    if slug == "01-statistical-methods":
        a = metrics["shingles"]["one_sample_results"]["A"]; b = metrics["shingles"]["one_sample_results"]["B"]
        return f"Shingle B is below the 0.35 limit by both t and Wilcoxon tests (t-test p={b['one_sided_t_p_value']:.4f}); Shingle A is not below the limit by the prespecified t-test (p={a['one_sided_t_p_value']:.3f})."
    if slug == "02-uber-drive-analysis":
        value = metrics["trip_summary"]; return f"After mixed-format date repair, {value['total_trips']:,} valid trips total {value['total_miles']:,.1f} miles; {value['business_mileage_share']:.1%} of recorded mileage is categorized as business."
    if slug == "03-anova-pca-analysis":
        edu = metrics["salary_inference"]["education"]; pca = metrics["pca"]; return f"Education shows a large observed salary association (eta²={edu['eta_squared']:.3f}); {pca['components_for_80_percent']} standardized components retain at least 80% of college-indicator variance."
    if slug == "04-insurance-claim-prediction":
        score = metrics["test_metrics_selected_threshold"]; return f"The tuned random forest selected by training PR-AUC reaches untouched-test ROC-AUC {score['roc_auc']:.3f}, PR-AUC {score['pr_auc']:.3f}, and balanced accuracy {score['balanced_accuracy']:.3f}."
    if slug == "05-gem-price-regression":
        score = metrics["test_metrics"]; interval = metrics["empirical_90_percent_interval"]; return f"Histogram gradient boosting reaches untouched-test R² {score['r_squared']:.3f}, RMSE {score['rmse']:,.0f}, and {interval['test_coverage']:.1%} coverage for the training-calibrated 90% diagnostic interval."
    if slug == "06-holiday-package-prediction":
        score = metrics["test_metrics"]; return f"Calibrated logistic regression reaches untouched-test ROC-AUC {score['roc_auc']:.3f} and PR-AUC {score['pr_auc']:.3f}; the high-recall training threshold produces {score['recall_sensitivity']:.1%} recall with low specificity."
    if slug == "07-election-exit-poll-prediction":
        score = metrics["test_metrics"]; return f"The calibrated random forest reaches retrospective test ROC-AUC {score['roc_auc']:.3f} and balanced accuracy {score['balanced_accuracy']:.3f}; this is respondent classification, not polling."
    if slug == "08-presidential-speech-analysis":
        pair = metrics["tfidf_similarity_pairs"][0]; return f"Kennedy 1961 and Nixon 1973 are the most similar tested pair by unigram/bigram TF-IDF cosine similarity ({pair['cosine_similarity']:.3f}), while topic and readability outputs remain exploratory."
    if slug == "09-wine-sales-forecasting":
        rose = metrics["products"]["rose"]; sparkling = metrics["products"]["sparkling"]; return f"Rolling-origin selection chooses {rose['selected_model'].replace('_', ' ')} for Rose (holdout RMSE {rose['final_holdout_metrics']['rmse']:.1f}) and additive Holt-Winters for Sparkling (RMSE {sparkling['final_holdout_metrics']['rmse']:.1f})."
    if slug == "10-marketing-retail-analysis":
        summary = metrics["business_summary"]; clustering = metrics["menu_item_segmentation"]; return f"The cleaned year contains {metrics['data_quality']['distinct_bills']:,} bills and {summary['recorded_revenue']:,.0f} recorded revenue units; two stable menu-item groups score {clustering['selected_silhouette']:.3f} silhouette."
    if slug == "11-parkinsons-disease-detection":
        score = metrics["participant_level_test_metrics"]; return f"With no participant overlap, the eight-person holdout has balanced accuracy {score['balanced_accuracy']:.3f}, sensitivity {score['recall_sensitivity']:.3f}, and specificity {score['specificity']:.3f}; uncertainty is necessarily wide."
    if slug == "12-online-retail-segmentation":
        selection = metrics["model_selection"]; return f"The pipeline segments {metrics['data_quality']['customers_segmented']:,} customers into {selection['selected_clusters']} stable RFM groups (silhouette {selection['selected_silhouette']:.3f}, seed ARI {selection['selected_seed_stability_ari']:.3f})."
    score = metrics["final_test_metrics"]
    return f"Across rolling origins, the seven-day rolling baseline remains best; final historical holdout RMSE is {score['rmse']:.1f} with {metrics['diagnostic_90_percent_interval']['final_test_coverage']:.1%} diagnostic interval coverage."


def markdown_cell(text: str) -> dict[str, object]:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code_cell(text: str) -> dict[str, object]:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)}


def _primary_table_markdown(project: Path, filename: str) -> str:
    path = project / "reports" / "tables" / filename
    if not path.is_file():
        return "Primary evidence table is generated during execution."
    import pandas as pd
    frame = pd.read_csv(path).head(10)
    def display(value: object) -> str:
        if pd.isna(value): return ""
        if isinstance(value, float): return f"{value:.3f}"
        return str(value).replace("|", "\\|").replace("\n", " ")
    header = "| " + " | ".join(map(str, frame.columns)) + " |"
    divider = "|" + "|".join("---" for _ in frame.columns) + "|"
    rows = ["| " + " | ".join(display(value) for value in row) + " |" for row in frame.itertuples(index=False, name=None)]
    return "\n".join([header, divider, *rows])


def render_readme(slug: str, meta: dict[str, str], metrics: dict[str, object]) -> str:
    result = result_summary(slug, metrics); project = ROOT / "projects" / slug
    table = _primary_table_markdown(project, meta["primary_table"])
    return f"""# {meta['title']}

> **Value proposition:** {meta['objective']}

![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg) ![Status](https://img.shields.io/badge/Status-Executed%20%26%20Validated-2ea44f.svg) ![Notebook](https://img.shields.io/badge/Notebook-Executed-F37626.svg)

## Executive summary

**Business question.** {meta['objective']}  
**Dataset.** {meta['dataset']}  
**Verified result.** {result}  
**Decision value.** {meta['decision']}  
**Primary limitation.** {metrics.get('limitation', metrics.get('limitations', metrics.get('responsible_use', 'See limitations below.')))}

![Primary evidence](reports/figures/{meta['figure']})

[Open the executed notebook](notebooks/01_end_to_end_analysis.ipynb) · [Inspect source code](src/analysis.py) · [Inspect metrics](reports/metrics.json) · [Original project](<{meta['original']}>)

## Business problem

The intended user is **{meta['user']}**. The analysis supports this decision: **{meta['decision']}** It does not claim causality or production readiness unless the study design supports that claim.

## Analytical questions and success criteria

1. What data-quality issues materially affect the analysis?
2. Which baseline establishes the minimum useful performance or descriptive reference?
3. Which method is selected under a leakage-safe validation design?
4. How stable, calibrated, or assumption-sensitive is the result?
5. What action is supported, and what action remains outside scope?

Technical success requires a fully executed pipeline, correct split logic, task-appropriate metrics, saved evidence, deterministic seeds where supported, and zero notebook errors. Business success requires an interpretable result that changes a defensible analytical decision without fabricating financial impact.

## Dataset and provenance

{meta['dataset']}

{meta['provenance']}

The exact local files, row counts, data types, missingness, cardinality, and checksums are exposed in the notebook and `reports/tables/*data_quality.csv`. Dataset terms must be reviewed separately from the repository's MIT code license.

## Methodology

{meta['methods']}

Reusable logic lives in `src/analysis.py`; the notebook imports and executes that same implementation. Preprocessing is fitted only inside training folds where a supervised model is used. Grouped and chronological projects keep entity and time boundaries intact.

## Validation strategy

```json
{json.dumps(metrics.get('validation', metrics.get('model_selection', dict())), indent=2)[:4500]}
```

## Verified result

> {result}

### Primary comparison table

{table}

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
| 1 | Use the verified result to prioritize a controlled analytical follow-up. | {result} | Better evidence for the stated decision | Observational or historical data may not generalize | Re-run on current data with a prespecified metric |
| 2 | Review the largest error, uncertainty, or sensitivity segment before deployment. | See saved diagnostic tables | Reduces hidden failure risk | Small subgroups can produce unstable estimates | Track subgroup error and interval coverage |
| 3 | Keep a transparent baseline in future monitoring. | Baseline comparison is recorded in the notebook | Detects when complexity stops adding value | Baselines do not capture every business driver | Compare every refresh against the same baseline |

## Limitations and responsible use

{metrics.get('limitation', metrics.get('limitations', 'See the executed metrics for project-specific limitations.'))}

{metrics.get('responsible_use', 'Treat outputs as educational analytical evidence and require domain review before operational use.')}

## Repository structure

```text
{slug}/
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
python projects/{slug}/src/analysis.py
python scripts/execute_notebooks.py --project {slug}
python validate_portfolio.py
```

Expected project runtime is hardware-dependent; the root reproducibility report records the measured portfolio run. Outputs are written under `projects/{slug}/reports/` and, for selected predictive models, `projects/{slug}/models/`.

## Technologies and skills demonstrated

Python 3.12/3.13 · pandas · NumPy · SciPy · scikit-learn · Matplotlib · OpenPyXL · Jupyter · data-quality engineering · {meta['problem']} · reproducibility · responsible interpretation.

## Future work

Acquire current, licensed, externally representative data; pre-register the primary metric and validation design; add domain-reviewed cost assumptions; and test the final approach prospectively before any operational use.

## Interview-ready explanation

“I rebuilt this as a {meta['problem'].lower()} case study. I began with provenance and data-quality risks, defined a baseline and validation design appropriate to the unit of observation, compared only justified methods, and accepted the result shown above even where a simpler baseline won. I then connected diagnostics and uncertainty to a specific stakeholder decision and documented where the evidence must not be used.”

## Résumé bullets

- Re-engineered a {meta['domain'].lower()} analysis into a reproducible {meta['problem'].lower()} workflow with automated data-quality evidence, saved outputs, and a fully executed recruiter-facing notebook.
- Implemented {meta['methods'].split(',')[0].lower()} and problem-appropriate validation to produce the verified result: {result}
- Translated model/statistical diagnostics into prioritized recommendations while documenting provenance, uncertainty, and responsible-use limits.
"""


def render_summary(slug: str, meta: dict[str, str], metrics: dict[str, object]) -> str:
    result = result_summary(slug, metrics)
    return f"""# Project Summary — {meta['title']}

| Item | Verified content |
|---|---|
| Business objective | {meta['objective']} |
| Problem type | {meta['problem']} |
| Dataset | {meta['dataset']} |
| Core methods | {meta['methods']} |
| Final result | {result} |
| Decision supported | {meta['decision']} |
| Primary evidence | `reports/figures/{meta['figure']}` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

{result} The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
"""


def render_data_readme(slug: str, meta: dict[str, str]) -> str:
    project = ROOT / "projects" / slug
    rows = []
    for path in sorted((project / "data").iterdir()):
        if not path.is_file() or path.name == "README.md": continue
        rows.append(f"| `{path.name}` | {path.stat().st_size:,} | `{hashlib.sha256(path.read_bytes()).hexdigest()}` |")
    return f"""# Data Documentation — {meta['title']}

## Scope

{meta['dataset']}

## Provenance and terms

{meta['provenance']}

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
{chr(10).join(rows)}

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
"""


def build_notebook(slug: str, meta: dict[str, str], metrics: dict[str, object]) -> dict[str, object]:
    project = ROOT / "projects" / slug; result = result_summary(slug, metrics)
    figures = sorted((project / "reports" / "figures").glob("*.png"))
    visual = "\n\n".join(f"### {path.stem.replace('_', ' ').title()}\n\n![{path.stem}](../reports/figures/{path.name})" for path in figures)
    setup = rf'''from pathlib import Path
import hashlib, importlib.util, json, os, platform, tempfile, time
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "portfolio-matplotlib-cache"))
import matplotlib, numpy as np, pandas as pd, scipy, sklearn
SLUG = {slug!r}
def locate_project():
    for base in [Path.cwd().resolve(), *Path.cwd().resolve().parents]:
        candidate = base if base.name == SLUG else base / "projects" / SLUG
        if (candidate / "src" / "analysis.py").is_file(): return candidate
    raise FileNotFoundError(SLUG)
PROJECT_ROOT = locate_project(); DATA_DIR = PROJECT_ROOT / "data"; REPORTS_DIR = PROJECT_ROOT / "reports"
print(pd.Series({{"Python": platform.python_version(), "pandas": pd.__version__, "NumPy": np.__version__, "SciPy": scipy.__version__, "scikit-learn": sklearn.__version__, "Matplotlib": matplotlib.__version__}}, name="version").to_string())
print(f"\nProject: {{PROJECT_ROOT.name}}")'''
    inventory = '''rows=[]
for path in sorted(DATA_DIR.iterdir()):
    if path.is_file() and path.name != "README.md": rows.append({"file": path.name, "size_mb": round(path.stat().st_size/1_000_000,3), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()[:16]})
inventory=pd.DataFrame(rows); print(inventory.to_string(index=False))'''
    preview = r'''def preview(path):
    if path.suffix.lower()==".csv": return pd.read_csv(path, nrows=5)
    if path.suffix.lower()==".xlsx": return pd.read_excel(path, nrows=5)
    return None
for path in sorted(DATA_DIR.iterdir()):
    frame=preview(path)
    if frame is None: continue
    for column in frame.select_dtypes(include="object"): frame[column]=frame[column].astype(str).str.replace(r"\\s+"," ",regex=True).str.slice(0,100)
    print(f"\n{path.name}: {frame.shape[1]} columns"); print(frame.to_string(index=False,max_cols=12))'''
    source = '''source_path=PROJECT_ROOT/"src"/"analysis.py"; text=source_path.read_text(encoding="utf-8")
print(f"Reusable implementation: {len(text.splitlines())} lines")
print("Functions:", ", ".join(line.split("(")[0].replace("def ","").strip() for line in text.splitlines() if line.startswith("def ")))'''
    execute = rf'''spec=importlib.util.spec_from_file_location("rebuilt_{slug.replace('-', '_')}", PROJECT_ROOT/"src"/"analysis.py")
analysis=importlib.util.module_from_spec(spec); spec.loader.exec_module(analysis)
started=time.perf_counter(); results=analysis.run_analysis(); runtime=time.perf_counter()-started
assert results["status"]=="passed"
print(f"Pipeline status: {{results['status']}}\nRuntime: {{runtime:.2f}} seconds")'''
    quality = r'''for path in sorted((REPORTS_DIR/"tables").glob("*data_quality.csv")):
    frame=pd.read_csv(path); print(f"\n{path.name} ({len(frame)} fields)"); print(frame.to_string(index=False,max_rows=30))'''
    evidence = rf'''primary=REPORTS_DIR/"tables"/{meta['primary_table']!r}
frame=pd.read_csv(primary); print(f"Primary evidence: {{primary.name}}, shape={{frame.shape}}")
print(frame.head(15).round(4).to_string(index=False))
print("\nVerified result:\n" + {result!r})'''
    robustness = r'''sections=[key for key in ["validation","model_selection","tuning","residual_diagnostics","outlier_sensitivity","participant_bootstrap_intervals","diagnostic_90_percent_interval","empirical_90_percent_interval"] if key in results]
for key in sections: print(f"\n{key.upper()}\n"+json.dumps(results[key],indent=2)[:6000])'''
    artifacts = '''rows=[]
for path in sorted(REPORTS_DIR.rglob("*")):
    if path.is_file(): rows.append({"artifact": str(path.relative_to(PROJECT_ROOT)), "size_kb": round(path.stat().st_size/1000,1), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()[:12]})
artifacts=pd.DataFrame(rows); print(artifacts.to_string(index=False,max_rows=80))'''
    acceptance = '''metrics=json.loads((REPORTS_DIR/"metrics.json").read_text(encoding="utf-8"))
assert metrics["status"]=="passed"
assert list((REPORTS_DIR/"figures").glob("*.png"))
assert list((REPORTS_DIR/"tables").glob("*.csv"))
assert all(path.stat().st_size>0 for path in REPORTS_DIR.rglob("*") if path.is_file())
print("PASS: metrics status, figures, tables, and non-empty artifacts verified")'''
    cells = [
        markdown_cell(f"# {meta['title']}\n\n**Recruiter-facing end-to-end analysis · {meta['problem']} · Python 3.12/3.13**\n\n> {result}"),
        markdown_cell(f"## Executive summary\n\n**Objective:** {meta['objective']}\n\n**Data:** {meta['dataset']}\n\n**Verified result:** {result}\n\n**Decision supported:** {meta['decision']}\n\nThe figures, tables, metrics, and execution counts in this notebook are saved outputs from the bundled data."),
        markdown_cell(f"## 1. Business understanding\n\n**Primary user:** {meta['user']}.\n\n**Decision:** {meta['decision']}\n\n**Why it matters:** A technically accurate result is useful only when its error costs, uncertainty, and decision boundary are visible. This project stays within the evidence available in the source data."),
        markdown_cell("## 2. Analytical objective and success criteria\n\nTechnical success requires portable execution, explicit data-quality evidence, a justified baseline, leakage-safe validation, task-appropriate metrics, diagnostics, and saved artifacts. Business success requires a specific recommendation supported by the observed result without invented financial impact."),
        markdown_cell("## 3. Reproducible environment"), code_cell(setup),
        markdown_cell(f"## 4. Data provenance and scope\n\n{meta['provenance']}\n\nThe next cells expose exact files, byte sizes, checksums, schemas, and sample records."),
        markdown_cell("### 4.1 Source-file inventory"), code_cell(inventory),
        markdown_cell("### 4.2 Raw-record and schema preview"), code_cell(preview),
        markdown_cell("## 5. Data-quality assessment\n\nThe pipeline checks missingness, duplicates, invalid fields, identifiers, cardinality, and problem-specific leakage or chronology risks. No row is silently removed."),
        markdown_cell("## 6. Reusable implementation\n\nLarge functions are kept in source code so the notebook remains a readable analytical narrative."), code_cell(source),
        markdown_cell(f"## 7. Methodology and hypotheses\n\n{meta['methods']}\n\nThe central hypothesis is that the audited features or group structure contain decision-relevant signal beyond the documented baseline. Exploratory findings are not presented as causal effects."),
        markdown_cell("## 8. Execute the complete pipeline\n\nThis cell reruns cleaning, feature engineering, model/statistical analysis, validation, tables, figures, and model artifacts."), code_cell(execute),
        markdown_cell("## 9. Executed data-quality evidence"), code_cell(quality),
        markdown_cell("## 10. Baseline, candidates, and primary result"), code_cell(evidence),
        markdown_cell("## 11. Validation, diagnostics, and robustness"), code_cell(robustness),
        markdown_cell(f"## 12. Visual evidence\n\n{visual}"),
        markdown_cell(f"## 13. Business interpretation\n\n{result}\n\nThe correct action is to use this result as evidence for **{meta['decision']}**, while retaining the documented baseline and monitoring the error or sensitivity segments."),
        markdown_cell("## 14. Prioritized recommendations\n\n1. Use the verified result to define a controlled follow-up rather than an automatic decision.\n2. Monitor the weakest subgroup, time window, interval coverage, or cluster sensitivity shown in the saved tables.\n3. Revalidate against a transparent baseline whenever the data or operating context changes."),
        markdown_cell(f"## 15. Limitations, ethics, and responsible use\n\n{metrics.get('limitation', metrics.get('limitations', metrics.get('responsible_use', 'See project README.')))}\n\nAutomated outputs remain associative unless a causal study design says otherwise."),
        markdown_cell("## 16. Saved-artifact integrity"), code_cell(artifacts),
        markdown_cell("## 17. Acceptance check"), code_cell(acceptance),
        markdown_cell(f"## 18. Conclusion\n\nThe project addressed {meta['objective'].lower()} using {meta['methods'].lower()} The final verified conclusion is: **{result}** The next responsible step is external or current-data validation before operational use."),
        markdown_cell(f"## 19. Reproduce locally\n\n```bash\npython projects/{slug}/src/analysis.py\npython scripts/execute_notebooks.py --project {slug}\n```"),
    ]
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}}, "nbformat": 4, "nbformat_minor": 5}


def main() -> None:
    for slug, meta in PROJECTS.items():
        project = ROOT / "projects" / slug
        metrics = json.loads((project / "reports" / "metrics.json").read_text(encoding="utf-8"))
        (project / "README.md").write_text(render_readme(slug, meta, metrics), encoding="utf-8")
        (project / "PROJECT_SUMMARY.md").write_text(render_summary(slug, meta, metrics), encoding="utf-8")
        (project / "data" / "README.md").write_text(render_data_readme(slug, meta), encoding="utf-8")
        notebook_path = project / "notebooks" / "01_end_to_end_analysis.ipynb"
        notebook_path.parent.mkdir(parents=True, exist_ok=True)
        notebook_path.write_text(json.dumps(build_notebook(slug, meta, metrics), indent=1), encoding="utf-8")
        legacy = project / "notebooks" / "analysis.ipynb"
        if legacy.is_file(): legacy.unlink()
        print(f"GENERATED {slug}")


if __name__ == "__main__":
    main()
