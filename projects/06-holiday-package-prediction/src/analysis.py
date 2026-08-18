"""Holiday-package propensity modeling with calibrated probabilities."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import joblib
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "portfolio-matplotlib-cache"))
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_validate, train_test_split
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_ROOT = ROOT.parents[1]
sys.path.insert(0, str(PORTFOLIO_ROOT))
from portfolio_lib import binary_metrics, classification_pipeline, data_quality_table, ensure_output_dirs, write_json

RANDOM_STATE = 42


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_csv(ROOT / "data" / "holiday_package.csv")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    data = raw.drop(columns=[column for column in raw.columns if column.lower().startswith("unnamed")])
    y = data.pop("Holliday_Package").str.lower().map({"no": 0, "yes": 1}).astype(int)
    X = data.copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    estimators = {
        "dummy_prevalence": DummyClassifier(strategy="prior"),
        "logistic_regression": LogisticRegression(max_iter=1500, class_weight="balanced", random_state=RANDOM_STATE),
        "linear_discriminant_analysis": LinearDiscriminantAnalysis(shrinkage="auto", solver="lsqr"),
        "decision_tree": DecisionTreeClassifier(max_depth=4, min_samples_leaf=15, class_weight="balanced", random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=350, min_samples_leaf=6, class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE),
        "gradient_boosting": GradientBoostingClassifier(n_estimators=120, learning_rate=0.035, max_depth=2, random_state=RANDOM_STATE),
    }
    models = {name: classification_pipeline(estimator, X) for name, estimator in estimators.items()}
    rows = []
    for name, model in models.items():
        scores = cross_validate(model, X_train, y_train, cv=cv, scoring={"pr_auc": "average_precision", "roc_auc": "roc_auc", "balanced_accuracy": "balanced_accuracy"}, n_jobs=-1)
        rows.append({
            "model": name,
            "cv_pr_auc_mean": float(scores["test_pr_auc"].mean()), "cv_pr_auc_std": float(scores["test_pr_auc"].std(ddof=1)),
            "cv_roc_auc_mean": float(scores["test_roc_auc"].mean()),
            "cv_balanced_accuracy_mean": float(scores["test_balanced_accuracy"].mean()),
        })
    comparison = pd.DataFrame(rows).sort_values("cv_pr_auc_mean", ascending=False).reset_index(drop=True)
    selected_name = str(comparison.loc[0, "model"])
    selected = models[selected_name]
    oof = cross_val_predict(clone(selected), X_train, y_train, cv=cv, method="predict_proba", n_jobs=-1)[:, 1]
    threshold_rows = []
    for threshold in np.arange(0.10, 0.76, 0.05):
        score = binary_metrics(y_train, oof, float(threshold))
        threshold_rows.append({"threshold": float(threshold), "precision": score["precision"], "recall": score["recall_sensitivity"], "f1": score["f1"]})
    thresholds = pd.DataFrame(threshold_rows)
    selected_threshold = float(thresholds.loc[thresholds["f1"].idxmax(), "threshold"])
    calibrated = CalibratedClassifierCV(estimator=clone(selected), cv=cv, method="sigmoid")
    calibrated.fit(X_train, y_train)
    probability = calibrated.predict_proba(X_test)[:, 1]
    test_metrics = binary_metrics(y_test, probability, selected_threshold)
    importance = permutation_importance(calibrated, X_test, y_test, scoring="average_precision", n_repeats=20, random_state=RANDOM_STATE, n_jobs=-1)
    importance_table = pd.DataFrame({"feature": X.columns, "importance": importance.importances_mean, "importance_std": importance.importances_std}).sort_values("importance", ascending=False)

    profile = data.assign(purchased=y).groupby("purchased").agg({"Salary": "median", "age": "mean", "educ": "mean", "no_young_children": "mean", "no_older_children": "mean"})
    comparison.to_csv(paths["tables"] / "model_comparison.csv", index=False)
    thresholds.to_csv(paths["tables"] / "campaign_thresholds.csv", index=False)
    importance_table.to_csv(paths["tables"] / "permutation_importance.csv", index=False)
    profile.to_csv(paths["tables"] / "customer_profile_by_outcome.csv")
    joblib.dump(calibrated, paths["models"] / "final_calibrated_model.joblib")

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    ordered = comparison.sort_values("cv_pr_auc_mean")
    axes[0, 0].barh(ordered["model"], ordered["cv_pr_auc_mean"], color="#2f6690")
    axes[0, 0].axvline(y_train.mean(), color="#d1495b", linestyle="--", label="purchase prevalence")
    axes[0, 0].set(title="Training CV model comparison", xlabel="Mean PR-AUC", xlim=(0, 1)); axes[0, 0].legend()
    axes[0, 1].plot(thresholds["threshold"], thresholds["precision"], marker="o", label="precision")
    axes[0, 1].plot(thresholds["threshold"], thresholds["recall"], marker="o", label="recall")
    axes[0, 1].plot(thresholds["threshold"], thresholds["f1"], marker="o", label="F1")
    axes[0, 1].axvline(selected_threshold, color="#d1495b", linestyle="--")
    axes[0, 1].set(title="Training-only campaign threshold trade-off", xlabel="Probability threshold", ylabel="Score", ylim=(0, 1)); axes[0, 1].legend()
    fraction, mean_prediction = calibration_curve(y_test, probability, n_bins=7, strategy="quantile")
    axes[1, 0].plot(mean_prediction, fraction, marker="o", color="#2f6690"); axes[1, 0].plot([0, 1], [0, 1], "--", color="#555555")
    axes[1, 0].set(title="Untouched-test calibration", xlabel="Predicted probability", ylabel="Observed purchase rate")
    top = importance_table.head(8).sort_values("importance")
    axes[1, 1].barh(top["feature"], top["importance"], color="#4f9d69")
    axes[1, 1].set(title="Permutation importance on untouched test", xlabel="Decrease in PR-AUC")
    fig.tight_layout(); fig.savefig(paths["figures"] / "holiday_propensity_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"rows": int(len(raw)), "columns": int(raw.shape[1]), "missing_cells": int(raw.isna().sum().sum()), "duplicate_rows": int(raw.duplicated().sum()), "purchase_prevalence": float(y.mean())},
        "validation": {"train_rows": int(len(X_train)), "untouched_test_rows": int(len(X_test)), "selection": "5-fold stratified CV on training data", "selection_metric": "PR-AUC", "random_seed": RANDOM_STATE},
        "candidate_models": comparison.to_dict(orient="records"), "selected_model": selected_name,
        "selected_threshold_from_training_oof": selected_threshold, "test_metrics": test_metrics,
        "top_permutation_features": importance_table.head(8).to_dict(orient="records"),
        "profile_by_observed_outcome": profile.round(3).to_dict(orient="index"),
        "decision_note": "Thresholds change contact volume and the precision-recall trade-off; business costs were unavailable, so the F1-optimal training threshold is illustrative rather than a profit optimum.",
        "responsible_use": "Use only as an educational propensity analysis; real campaigns require consent, fairness review, frequency limits, and current validation.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
