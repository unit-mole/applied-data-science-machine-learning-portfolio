# Project Summary — Participant-Safe Parkinson's Voice Classification

| Item | Verified content |
|---|---|
| Business objective | Evaluate voice-based classification without allowing recordings from one participant to cross train/test boundaries. |
| Problem type | Grouped high-stakes classification |
| Dataset | 195 recordings, 22 acoustic features, and 32 derived participant identifiers. |
| Core methods | Participant-level holdout, StratifiedGroupKFold selection, dummy/logistic/SVM/forest/boosting comparison, recording and participant metrics, bootstrap intervals, false-negative review, and permutation importance. |
| Final result | With no participant overlap, the eight-person holdout has balanced accuracy 0.750, sensitivity 1.000, and specificity 0.500; uncertainty is necessarily wide. |
| Decision supported | Judge whether signal warrants external study—not make a clinical decision. |
| Primary evidence | `reports/figures/participant_safe_model_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

With no participant overlap, the eight-person holdout has balanced accuracy 0.750, sensitivity 1.000, and specificity 0.500; uncertainty is necessarily wide. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
