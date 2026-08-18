# Project Summary — Cafe Marketing and Retail Analytics

| Item | Verified content |
|---|---|
| Business objective | Translate point-of-sale lines into revenue, order, daypart, basket, and stable menu-item insights supported by available fields. |
| Problem type | Transactional business analysis and item segmentation |
| Dataset | 145,830 cafe line items covering 69,982 bills and one year of activity. |
| Core methods | Duplicate control, monthly/category/daypart KPIs, order-value analysis, bill-level pair support/confidence/lift, and stable K-means menu-item segmentation. |
| Final result | The cleaned year contains 69,982 bills and 32,654,640 recorded revenue units; two stable menu-item groups score 0.395 silhouette. |
| Decision supported | Prioritize menu review, daypart staffing, and carefully tested cross-sell ideas. |
| Primary evidence | `reports/figures/cafe_business_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

The cleaned year contains 69,982 bills and 32,654,640 recorded revenue units; two stable menu-item groups score 0.395 silhouette. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
