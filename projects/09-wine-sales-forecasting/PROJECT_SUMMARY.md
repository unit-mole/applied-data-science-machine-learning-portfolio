# Project Summary — Wine Sales Forecasting with Rolling-Origin Validation

| Item | Verified content |
|---|---|
| Business objective | Select transparent monthly forecasting methods on multiple historical origins and evaluate once on a final 24-month holdout. |
| Problem type | Monthly time-series forecasting |
| Dataset | 187 monthly Rose and Sparkling observations from January 1980 through July 1995. |
| Core methods | Frequency audit, train-contained interpolation, seasonal-naive baseline, trend/month regression, lagged ridge, additive Holt-Winters implementation, three rolling origins, empirical intervals, and Ljung–Box residual autocorrelation. |
| Final result | Rolling-origin selection chooses trend plus month for Rose (holdout RMSE 13.6) and additive Holt-Winters for Sparkling (RMSE 358.7). |
| Decision supported | Choose a reproducible baseline and quantify forecast risk before inventory commitment. |
| Primary evidence | `reports/figures/wine_forecasting_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

Rolling-origin selection chooses trend plus month for Rose (holdout RMSE 13.6) and additive Holt-Winters for Sparkling (RMSE 358.7). The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
