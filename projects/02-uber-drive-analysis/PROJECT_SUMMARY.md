# Project Summary — Uber Drive Behavior and Productivity Analysis

| Item | Verified content |
|---|---|
| Business objective | Audit and summarize a personal trip log to expose temporal, purpose, route, and distance patterns without inventing a prediction target. |
| Problem type | Decision-oriented exploratory analysis |
| Dataset | 1,155 source rows containing trip timestamps, categories, locations, distance, and purpose. |
| Core methods | Mixed-format datetime repair, data-quality rules, duration and speed checks, temporal aggregation, route concentration, missing-purpose analysis, and IQR outlier review. |
| Final result | After mixed-format date repair, 1,154 valid trips total 12,194.8 miles; 94.1% of recorded mileage is categorized as business. |
| Decision supported | Improve purpose capture, route scheduling, mileage review, and reimbursement evidence. |
| Primary evidence | `reports/figures/uber_trip_behavior_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

After mixed-format date repair, 1,154 valid trips total 12,194.8 miles; 94.1% of recorded mileage is categorized as business. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
