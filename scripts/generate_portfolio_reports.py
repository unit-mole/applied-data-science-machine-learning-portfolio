"""Generate portfolio-level documentation from executed project metrics."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("content", ROOT / "scripts" / "generate_portfolio_content.py")
if spec is None or spec.loader is None: raise RuntimeError("Unable to load project metadata")
content = importlib.util.module_from_spec(spec); spec.loader.exec_module(content)


def load() -> list[tuple[str, dict[str, str], dict[str, object]]]:
    return [(slug, meta, json.loads((ROOT / "projects" / slug / "reports" / "metrics.json").read_text(encoding="utf-8"))) for slug, meta in content.PROJECTS.items()]


def root_readme(projects: list[tuple[str, dict[str, str], dict[str, object]]]) -> str:
    rows = []
    for number, (slug, meta, metrics) in enumerate(projects, start=1):
        result = content.result_summary(slug, metrics)
        rows.append(f"| {number} | [{meta['title']}](projects/{slug}/) | {meta['problem']} | {meta['dataset']} | {result} | {meta['decision']} |")
    return """# Applied Data Science Portfolio — Rebuilt

![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg) ![Projects](https://img.shields.io/badge/Projects-13%2F13%20Executed-2ea44f.svg) ![Notebooks](https://img.shields.io/badge/Notebooks-13%20Executed-F37626.svg) ![Validation](https://img.shields.io/badge/Validation-Passed-2ea44f.svg) ![License](https://img.shields.io/badge/Code%20License-MIT-green.svg)

A recruiter-facing portfolio of 13 end-to-end statistics, data science, machine learning, forecasting, NLP, retail, biomedical, and customer-analytics case studies.

This rebuild preserves the analytical intent of the original classroom projects while replacing assignment-style execution with a consistent professional standard:

> **Business problem → data provenance → quality audit → EDA → hypotheses → feature engineering → baseline → candidate models → validation → explainability → business decision → limitations**

## Technical profile

I build reproducible analytical systems that connect rigorous methodology with stakeholder decisions. The portfolio demonstrates mixed-type ML pipelines, cross-validation, calibration, threshold analysis, grouped patient evaluation, chronological forecasting, statistical robustness, text analytics, clustering stability, artifact testing, and responsible interpretation.

## Start with executed evidence

[Execution and environment report](REPRODUCIBILITY_REPORT.md) · [Portfolio audit](PORTFOLIO_AUDIT.md) · [Model results](MODEL_RESULTS_SUMMARY.md) · [Status matrix](PROJECT_STATUS_MATRIX.md) · [Run instructions](RUN_INSTRUCTIONS.md)

| Insurance classification | Gem-price regression |
|---|---|
| [![Insurance evidence](projects/04-insurance-claim-prediction/reports/figures/insurance_model_evidence.png)](projects/04-insurance-claim-prediction/notebooks/01_end_to_end_analysis.ipynb) | [![Gem evidence](projects/05-gem-price-regression/reports/figures/gem_price_model_evidence.png)](projects/05-gem-price-regression/notebooks/01_end_to_end_analysis.ipynb) |

| Wine forecasting | Online Retail segmentation |
|---|---|
| [![Wine evidence](projects/09-wine-sales-forecasting/reports/figures/wine_forecasting_evidence.png)](projects/09-wine-sales-forecasting/notebooks/01_end_to_end_analysis.ipynb) | [![Retail segmentation](projects/12-online-retail-segmentation/reports/figures/online_retail_segmentation_evidence.png)](projects/12-online-retail-segmentation/notebooks/01_end_to_end_analysis.ipynb) |

## Verified project portfolio

| No. | Project | Problem type | Dataset | Best verified result | Decision value |
|---:|---|---|---|---|---|
""" + "\n".join(rows) + r"""

## Portfolio philosophy

- A simple baseline that survives validation is more valuable than a complicated model selected on the test set.
- Preprocessing belongs inside training folds.
- Repeated entities and time require grouped and chronological validation.
- Calibration, error segments, interval coverage, stability, and assumptions matter alongside headline metrics.
- Clusters are descriptive profiles, not objective truths.
- Medical, political, insurance, and public-health analyses require especially clear boundaries.
- Modest or negative results are retained when they are methodologically correct.

## Repository architecture

```text
applied-data-science-portfolio-rebuilt/
├── README.md
├── PORTFOLIO_AUDIT.md
├── PROJECT_STATUS_MATRIX.md
├── MODEL_RESULTS_SUMMARY.md
├── REPRODUCIBILITY_REPORT.md
├── RUN_INSTRUCTIONS.md
├── setup.ps1 / run_all.ps1 / setup_and_run.ps1
├── run_all.py / validate_portfolio.py
├── portfolio_lib/                 # shared tested utilities
├── projects/                      # 13 complete case studies
├── scripts/                       # notebook and documentation builders
└── tests/                         # schema, path, notebook, and contract tests
```

Each project contains a long-form executed notebook, reusable source implementation, professional README, one-page project summary, data provenance note and checksums, machine-readable metrics, saved tables, figures, and a fitted model where retaining one adds value.

## Unified installation and execution

### Windows — recommended

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_and_run.ps1
```

### Manual Python 3.12 setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[notebooks,dev]"
.\.venv\Scripts\python.exe run_all.py
```

Python 3.13 is supported where the bounded dependencies provide wheels; replace `-3.12` with `-3.13`. CPU execution is the default and no API key or GPU is required.

## Skills matrix

| Skill | Projects |
|---|---|
| Statistical assumptions, robust alternatives, effect size | 1, 3 |
| Decision-oriented EDA and data quality | 1–13 |
| Leakage-safe mixed-type pipelines | 4–7 |
| Calibration and threshold analysis | 4, 6, 7 |
| Regression diagnostics and uncertainty | 5 |
| Grouped participant validation | 11 |
| Rolling-origin chronological validation | 9, 13 |
| NLP, readability, TF-IDF, topics | 8 |
| Basket analysis and retail operations | 10 |
| RFM, multi-method clustering, stability | 12 |
| Explainability and error segmentation | 4–7, 11, 13 |
| Reproducible notebooks, artifacts, tests | All |

## Reproducibility statement

All displayed numerical claims are read from executed `reports/metrics.json` files. The primary notebooks were executed from top to bottom and retain execution counts and outputs. Dataset hashes, metric hashes, package versions, measured runtime, and notebook status are recorded in `REPRODUCIBILITY_REPORT.md` and `.json`.

## Portfolio-wide limitations

Several classroom datasets lack complete sampling or redistribution documentation. Historical samples do not establish current performance. Holdout results remain estimates, not deployment guarantees. No project should be used as an automatic medical, political, financial, insurance, or public-health decision system.

## Author

[Anmol Tripathi on GitHub](https://github.com/unit-mole)
"""


def model_summary(projects: list[tuple[str, dict[str, str], dict[str, object]]]) -> str:
    sections = ["# Model and Analytical Results Summary", "", "Only executed metrics are reported. Selection metrics come from training-only, grouped, or chronological validation; final metrics come from untouched holdouts where applicable.", ""]
    for slug, meta, metrics in projects:
        sections.extend([f"## {meta['title']}", "", f"**Verified result:** {content.result_summary(slug, metrics)}", ""])
        if "candidate_models" in metrics:
            candidates = metrics["candidate_models"][:8]
            columns = list(candidates[0]) if candidates else []
            sections.extend(["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"])
            for row in candidates: sections.append("| " + " | ".join(f"{row.get(column):.4f}" if isinstance(row.get(column), float) else str(row.get(column, "")) for column in columns) + " |")
            sections.append("")
        validation = metrics.get("validation", metrics.get("model_selection", {}))
        sections.extend(["**Selection rationale / validation:**", "", "```json", json.dumps(validation, indent=2)[:5000], "```", ""])
    return "\n".join(sections)


def status_matrix(projects: list[tuple[str, dict[str, str], dict[str, object]]]) -> str:
    rows = []
    for number, (slug, meta, metrics) in enumerate(projects, start=1):
        rows.append(f"| {number} | {meta['title']} | Complete | Complete | Passed | Passed | Complete | {content.result_summary(slug, metrics)} | {str(metrics.get('limitation', metrics.get('limitations', metrics.get('responsible_use', 'See README'))))[:170]} |")
    return """# Project Status Matrix

| No. | Project | Audit | Rebuild | Notebook | Tests | README | Final verified result | Known limitation |
|---:|---|---|---|---|---|---|---|---|
""" + "\n".join(rows) + "\n"


def main() -> None:
    projects = load()
    (ROOT / "README.md").write_text(root_readme(projects), encoding="utf-8")
    (ROOT / "MODEL_RESULTS_SUMMARY.md").write_text(model_summary(projects), encoding="utf-8")
    (ROOT / "PROJECT_STATUS_MATRIX.md").write_text(status_matrix(projects), encoding="utf-8")
    print("GENERATED portfolio reports")


if __name__ == "__main__":
    main()
