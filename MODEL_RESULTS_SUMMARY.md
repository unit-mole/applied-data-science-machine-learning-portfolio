# Model and Analytical Results Summary

Only executed metrics are reported. Selection metrics come from training-only, grouped, or chronological validation; final metrics come from untouched holdouts where applicable.

## Statistical Methods for Decision-Making

**Verified result:** Shingle B is below the 0.35 limit by both t and Wilcoxon tests (t-test p=0.0021); Shingle A is not below the limit by the prespecified t-test (p=0.075).

**Selection rationale / validation:**

```json
{}
```

## Uber Drive Behavior and Productivity Analysis

**Verified result:** After mixed-format date repair, 1,154 valid trips total 12,194.8 miles; 94.1% of recorded mileage is categorized as business.

**Selection rationale / validation:**

```json
{}
```

## Salary Factor Analysis and College Admissions PCA

**Verified result:** Education shows a large observed salary association (eta²=0.626); 6 standardized components retain at least 80% of college-indicator variance.

**Selection rationale / validation:**

```json
{}
```

## Insurance Claim Propensity Modeling

**Verified result:** The tuned random forest selected by training PR-AUC reaches untouched-test ROC-AUC 0.799, PR-AUC 0.613, and balanced accuracy 0.713.

| model | cv_pr_auc_mean | cv_pr_auc_std | cv_roc_auc_mean | cv_balanced_accuracy_mean | selection_stage |
|---|---|---|---|---|---|
| random_forest_tuned | 0.6818 | None | None | None | randomized_search_8_candidates |
| random_forest | 0.6731 | 0.0369 | 0.8120 | 0.7438 | candidate |
| logistic_regression | 0.6710 | 0.0580 | 0.8103 | 0.7445 | candidate |
| gradient_boosting | 0.6634 | 0.0489 | 0.8084 | 0.6991 | candidate |
| mlp | 0.6539 | 0.0795 | 0.7851 | 0.6804 | candidate |
| decision_tree | 0.6238 | 0.0512 | 0.7926 | 0.7211 | candidate |
| dummy_prevalence | 0.3193 | 0.0006 | 0.5000 | 0.5000 | candidate |

**Selection rationale / validation:**

```json
{
  "train_rows": 2145,
  "untouched_test_rows": 716,
  "test_fraction": 0.25,
  "selection_cv": "4-fold stratified CV on training data only",
  "optimization_metric": "average precision (PR-AUC)",
  "random_seed": 42
}
```

## Cubic Zirconia Price Modeling

**Verified result:** Histogram gradient boosting reaches untouched-test R² 0.981, RMSE 563, and 90.6% coverage for the training-calibrated 90% diagnostic interval.

| model | cv_rmse_mean | cv_rmse_std | cv_mae_mean | cv_r_squared_mean |
|---|---|---|---|---|
| hist_gradient_boosting | 573.3211 | 30.0947 | 299.7832 | 0.9795 |
| random_forest | 594.7283 | 27.0487 | 298.8835 | 0.9779 |
| log_target_ridge | 921.8108 | 81.0471 | 443.5555 | 0.9467 |
| linear_regression | 1128.5471 | 31.8824 | 742.0371 | 0.9205 |
| median_baseline | 4293.9194 | 49.7442 | 2815.6583 | -0.1497 |

**Selection rationale / validation:**

```json
{
  "training_rows": 21573,
  "untouched_test_rows": 5394,
  "model_selection": "4-fold shuffled CV on training only",
  "calibration_rows_for_interval": 4315,
  "random_seed": 42
}
```

## Holiday Package Purchase Propensity

**Verified result:** Calibrated logistic regression reaches untouched-test ROC-AUC 0.730 and PR-AUC 0.707; the high-recall training threshold produces 93.0% recall with low specificity.

| model | cv_pr_auc_mean | cv_pr_auc_std | cv_roc_auc_mean | cv_balanced_accuracy_mean |
|---|---|---|---|---|
| logistic_regression | 0.7136 | 0.0319 | 0.7240 | 0.6642 |
| gradient_boosting | 0.7096 | 0.0499 | 0.7364 | 0.6611 |
| linear_discriminant_analysis | 0.7080 | 0.0311 | 0.7210 | 0.6576 |
| random_forest | 0.6988 | 0.0423 | 0.7287 | 0.6729 |
| decision_tree | 0.6364 | 0.0208 | 0.6908 | 0.6291 |
| dummy_prevalence | 0.4602 | 0.0034 | 0.5000 | 0.5000 |

**Selection rationale / validation:**

```json
{
  "train_rows": 654,
  "untouched_test_rows": 218,
  "selection": "5-fold stratified CV on training data",
  "selection_metric": "PR-AUC",
  "random_seed": 42
}
```

## Retrospective Election Survey Classification

**Verified result:** The calibrated random forest reaches retrospective test ROC-AUC 0.909 and balanced accuracy 0.806; this is respondent classification, not polling.

| model | cv_roc_auc_mean | cv_roc_auc_std | cv_balanced_accuracy_mean | cv_f1_mean |
|---|---|---|---|---|
| random_forest | 0.8836 | 0.0255 | 0.8043 | 0.8530 |
| linear_discriminant_analysis | 0.8811 | 0.0169 | 0.7832 | 0.8789 |
| support_vector_machine | 0.8797 | 0.0295 | 0.8139 | 0.8598 |
| logistic_regression | 0.8790 | 0.0174 | 0.8078 | 0.8549 |
| knn | 0.8723 | 0.0279 | 0.7758 | 0.8771 |
| dummy_majority | 0.5000 | 0.0000 | 0.5000 | 0.8216 |

**Selection rationale / validation:**

```json
{
  "training_rows": 1143,
  "untouched_test_rows": 382,
  "selection": "5-fold stratified CV on training only",
  "selection_metric": "ROC-AUC",
  "random_seed": 42
}
```

## U.S. Presidential Inaugural Speech Analysis

**Verified result:** Kennedy 1961 and Nixon 1973 are the most similar tested pair by unigram/bigram TF-IDF cosine similarity (0.114), while topic and readability outputs remain exploratory.

**Selection rationale / validation:**

```json
{}
```

## Wine Sales Forecasting with Rolling-Origin Validation

**Verified result:** Rolling-origin selection chooses trend plus month for Rose (holdout RMSE 13.6) and additive Holt-Winters for Sparkling (RMSE 358.7).

**Selection rationale / validation:**

```json
{
  "model_selection": "three rolling-origin 12-month validation windows",
  "final_holdout": "last 24 months, untouched during selection",
  "missing_rose_values": "linear interpolation within the series; neither missing record is in the final holdout"
}
```

## Cafe Marketing and Retail Analytics

**Verified result:** The cleaned year contains 69,982 bills and 32,654,640 recorded revenue units; two stable menu-item groups score 0.395 silhouette.

**Selection rationale / validation:**

```json
{}
```

## Participant-Safe Parkinson's Voice Classification

**Verified result:** With no participant overlap, the eight-person holdout has balanced accuracy 0.750, sensitivity 1.000, and specificity 0.500; uncertainty is necessarily wide.

| model | participant_cv_roc_auc_mean | participant_cv_roc_auc_std | participant_cv_balanced_accuracy_mean | participant_cv_recall_mean |
|---|---|---|---|---|
| gradient_boosting | 0.7812 | 0.1375 | 0.6000 | 0.9500 |
| logistic_regression | 0.5875 | 0.4211 | 0.5750 | 0.7750 |
| random_forest | 0.5500 | 0.3894 | 0.5938 | 0.9375 |
| support_vector_machine | 0.5375 | 0.4888 | 0.5938 | 0.9375 |
| dummy_prevalence | 0.5000 | 0.1021 | 0.5000 | 1.0000 |

**Selection rationale / validation:**

```json
{
  "train_participants": 24,
  "held_out_participants": 8,
  "same_participant_in_train_and_test": false,
  "model_selection": "4-fold StratifiedGroupKFold on training participants",
  "random_seed": 42
}
```

## Online Retail Customer Segmentation

**Verified result:** The pipeline segments 4,338 customers into 2 stable RFM groups (silhouette 0.432, seed ARI 0.999).

**Selection rationale / validation:**

```json
{
  "methods": [
    "K-means",
    "Gaussian mixture"
  ],
  "candidate_clusters": [
    2,
    3,
    4,
    5,
    6,
    7
  ],
  "selection_rule": "composite rank among K-means candidates with >=5% smallest segment and >=0.80 seed ARI",
  "selected_clusters": 2,
  "selected_silhouette": 0.4323284246768482,
  "selected_davies_bouldin": 0.8924990931024944,
  "selected_calinski_harabasz": 4367.323097619211,
  "selected_seed_stability_ari": 0.9990752738031528
}
```

## Historical COVID-19 Next-Day Case Modeling

**Verified result:** Across rolling origins, the seven-day rolling baseline remains best; final historical holdout RMSE is 388.2 with 89.6% diagnostic interval coverage.

| model | mean_rmse | std_rmse | mean_mae | mean_r_squared |
|---|---|---|---|---|
| rolling_7_baseline | 499.8500 | 87.2231 | 89.8868 | 0.9465 |
| last_value | 570.8421 | 177.5552 | 88.2142 | 0.9259 |
| hist_gradient_boosting_lags | 908.7679 | 483.6822 | 125.2566 | 0.7998 |
| ridge_country_lags | 22190367281232.2305 | 38434842478420.1250 | 663709794902.9479 | -293758145618887606272.0000 |

**Selection rationale / validation:**

```json
{
  "selection": "three rolling-origin 14-day windows",
  "final_holdout_start": "2020-05-11",
  "final_holdout_end": "2020-05-24",
  "final_train_rows": 14890,
  "final_test_rows": 2917,
  "random_seed": 42
}
```
