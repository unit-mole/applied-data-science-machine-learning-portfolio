# Delivery Report

## Delivered scope

This release contains 13 rebuilt projects. Each project includes a professional README, project summary, source data notes, an executable Python pipeline, a substantial executed notebook, saved figures, saved tables, and structured metrics. Predictive projects include persisted models when reuse is appropriate.

## Evaluation safeguards

- Classification/regression: training-only preprocessing, candidate comparison, explicit baselines, and untouched test evaluation.
- Parkinson's: participant-grouped selection and holdout, with zero participant overlap.
- Wine and COVID-19: chronological rolling validation and untouched final periods.
- Segmentation: internal validation, seed stability, and outlier-sensitivity checks.
- Statistical projects: assumptions, robust alternatives, effect sizes, multiple-testing correction, and practical interpretation.

## Portfolio evidence

- [Portfolio audit](PORTFOLIO_AUDIT.md)
- [Project status matrix](PROJECT_STATUS_MATRIX.md)
- [Model results summary](MODEL_RESULTS_SUMMARY.md)
- [Reproducibility report](REPRODUCIBILITY_REPORT.md)
- [Run instructions](RUN_INSTRUCTIONS.md)

## Acceptance criteria

The release is accepted only when all 13 projects report `passed`, every notebook has saved execution counts and outputs, no notebook contains an error output, repository validation passes, automated tests pass, and the final archive passes an integrity test. The final validation results are recorded in the reproducibility report and execution-log summary.
