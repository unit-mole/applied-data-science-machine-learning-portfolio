# Reproducibility Report

**Status:** Passed  
**Executed at (UTC):** 2026-08-18T17:16:41+00:00  
**Python:** 3.12.13  
**Projects:** 13  
**Total measured notebook runtime:** 208.7 seconds

## Scientific environment

| Package | Version |
|---|---:|
| numpy | 2.3.5 |
| pandas | 2.2.3 |
| scipy | 1.17.0 |
| scikit-learn | 1.8.0 |
| matplotlib | 3.10.8 |
| openpyxl | 3.1.5 |

## Notebook execution evidence

| Project | Status | Cells | Code cells | Code cells with output | Runtime | Notebook | Metrics | Figures | Tables |
|---|---|---:|---:|---:|---:|---|---|---:|---:|
| 01-statistical-methods | Passed | 33 | 10 | 9 | 1.9s | [Notebook](projects/01-statistical-methods/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/01-statistical-methods/reports/metrics.json) | 2 | 7 |
| 02-uber-drive-analysis | Passed | 33 | 10 | 9 | 0.7s | [Notebook](projects/02-uber-drive-analysis/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/02-uber-drive-analysis/reports/metrics.json) | 2 | 6 |
| 03-anova-pca-analysis | Passed | 33 | 10 | 9 | 0.6s | [Notebook](projects/03-anova-pca-analysis/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/03-anova-pca-analysis/reports/metrics.json) | 2 | 5 |
| 04-insurance-claim-prediction | Passed | 33 | 10 | 10 | 64.0s | [Notebook](projects/04-insurance-claim-prediction/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/04-insurance-claim-prediction/reports/metrics.json) | 2 | 4 |
| 05-gem-price-regression | Passed | 33 | 10 | 10 | 10.3s | [Notebook](projects/05-gem-price-regression/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/05-gem-price-regression/reports/metrics.json) | 2 | 5 |
| 06-holiday-package-prediction | Passed | 33 | 10 | 10 | 3.1s | [Notebook](projects/06-holiday-package-prediction/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/06-holiday-package-prediction/reports/metrics.json) | 2 | 5 |
| 07-election-exit-poll-prediction | Passed | 33 | 10 | 10 | 46.6s | [Notebook](projects/07-election-exit-poll-prediction/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/07-election-exit-poll-prediction/reports/metrics.json) | 2 | 4 |
| 08-presidential-speech-analysis | Passed | 33 | 10 | 9 | 0.8s | [Notebook](projects/08-presidential-speech-analysis/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/08-presidential-speech-analysis/reports/metrics.json) | 2 | 6 |
| 09-wine-sales-forecasting | Passed | 33 | 10 | 10 | 0.7s | [Notebook](projects/09-wine-sales-forecasting/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/09-wine-sales-forecasting/reports/metrics.json) | 2 | 7 |
| 10-marketing-retail-analysis | Passed | 33 | 10 | 9 | 11.1s | [Notebook](projects/10-marketing-retail-analysis/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/10-marketing-retail-analysis/reports/metrics.json) | 2 | 8 |
| 11-parkinsons-disease-detection | Passed | 33 | 10 | 10 | 26.9s | [Notebook](projects/11-parkinsons-disease-detection/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/11-parkinsons-disease-detection/reports/metrics.json) | 2 | 4 |
| 12-online-retail-segmentation | Passed | 33 | 10 | 10 | 39.7s | [Notebook](projects/12-online-retail-segmentation/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/12-online-retail-segmentation/reports/metrics.json) | 2 | 5 |
| 13-covid-outbreak-prediction | Passed | 33 | 10 | 10 | 2.4s | [Notebook](projects/13-covid-outbreak-prediction/notebooks/01_end_to_end_analysis.ipynb) | [Metrics](projects/13-covid-outbreak-prediction/reports/metrics.json) | 2 | 5 |

All primary notebooks load bundled data, expose provenance and quality evidence, execute the complete reusable pipeline, show task-appropriate results and robustness evidence, embed saved figures, and verify artifact hashes. Runtime varies by CPU and installed library versions.

## Determinism and known variation

Random seeds are fixed where supported. Parallel tree fitting, numerical libraries, and dependency-version changes can cause small floating-point differences. Dataset hashes and metric hashes are recorded so material drift can be distinguished from harmless numeric variation.
