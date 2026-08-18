# Project Summary — Historical COVID-19 Next-Day Case Modeling

| Item | Verified content |
|---|---|
| Business objective | Compare lag-only one-day-ahead models with transparent baselines across multiple chronological windows. |
| Problem type | Historical panel forecasting |
| Dataset | 19,496 country-date rows from December 2019 through May 2020 with cases, tests, policy, population, and demographic fields. |
| Core methods | Revision audit, lag/rolling features, three 14-day rolling origins, last-value and rolling baselines, country-aware ridge, histogram boosting, final chronological holdout, diagnostic intervals, and country-level error analysis. |
| Final result | Across rolling origins, the seven-day rolling baseline remains best; final historical holdout RMSE is 388.2 with 89.6% diagnostic interval coverage. |
| Decision supported | Assess baseline adequacy and reporting risk—not make a current forecast or policy recommendation. |
| Primary evidence | `reports/figures/historical_covid_validation_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

Across rolling origins, the seven-day rolling baseline remains best; final historical holdout RMSE is 388.2 with 89.6% diagnostic interval coverage. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
