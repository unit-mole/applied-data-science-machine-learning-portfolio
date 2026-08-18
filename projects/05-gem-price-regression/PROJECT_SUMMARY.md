# Project Summary — Cubic Zirconia Price Modeling

| Item | Verified content |
|---|---|
| Business objective | Compare interpretable and nonlinear price models, diagnose residual risk, and quantify empirical prediction coverage. |
| Problem type | Supervised regression |
| Dataset | 26,967 cubic-zirconia records with physical measurements, quality grades, and price. |
| Core methods | Leakage-safe imputation/encoding, median baseline, linear and regularized log-target models, random forest, histogram boosting, cross-validation, residual diagnostics, permutation importance, segment errors, and calibration-residual intervals. |
| Final result | Histogram gradient boosting reaches untouched-test R² 0.981, RMSE 563, and 90.6% coverage for the training-calibrated 90% diagnostic interval. |
| Decision supported | Estimate price ranges and identify where prediction errors become operationally material. |
| Primary evidence | `reports/figures/gem_price_model_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

Histogram gradient boosting reaches untouched-test R² 0.981, RMSE 563, and 90.6% coverage for the training-calibrated 90% diagnostic interval. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
