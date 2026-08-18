"""Retrospective election-survey classification with calibrated validation."""

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
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import binary_metrics, classification_pipeline, data_quality_table, ensure_output_dirs, write_json

RANDOM_STATE = 42


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_excel(ROOT / "data" / "election_data.xlsx")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    data = raw.drop(columns=[column for column in raw.columns if column.lower().startswith("unnamed")])
    y = data.pop("vote").map({"Conservative": 0, "Labour": 1}).astype(int)
    X = data.copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    estimators = {
        "dummy_majority": DummyClassifier(strategy="prior"),
        "logistic_regression": LogisticRegression(max_iter=1500, class_weight="balanced", random_state=RANDOM_STATE),
        "linear_discriminant_analysis": LinearDiscriminantAnalysis(shrinkage="auto", solver="lsqr"),
        "knn": KNeighborsClassifier(n_neighbors=19, weights="distance"),
        "support_vector_machine": SVC(C=1.0, kernel="rbf", class_weight="balanced", probability=True, random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=400, min_samples_leaf=5, class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE),
    }
    models = {name: classification_pipeline(estimator, X) for name, estimator in estimators.items()}
    rows = []
    for name, model in models.items():
        scores = cross_validate(model, X_train, y_train, cv=cv, scoring={"roc_auc": "roc_auc", "balanced_accuracy": "balanced_accuracy", "f1": "f1"}, n_jobs=-1)
        rows.append({
            "model": name, "cv_roc_auc_mean": float(scores["test_roc_auc"].mean()),
            "cv_roc_auc_std": float(scores["test_roc_auc"].std(ddof=1)),
            "cv_balanced_accuracy_mean": float(scores["test_balanced_accuracy"].mean()),
            "cv_f1_mean": float(scores["test_f1"].mean()),
        })
    comparison = pd.DataFrame(rows).sort_values("cv_roc_auc_mean", ascending=False).reset_index(drop=True)
    selected_name = str(comparison.loc[0, "model"])
    calibrated = CalibratedClassifierCV(estimator=clone(models[selected_name]), cv=cv, method="sigmoid")
    calibrated.fit(X_train, y_train)
    probability = calibrated.predict_proba(X_test)[:, 1]
    test_metrics = binary_metrics(y_test, probability)

    importance = permutation_importance(calibrated, X_test, y_test, scoring="roc_auc", n_repeats=20, random_state=RANDOM_STATE, n_jobs=-1)
    importance_table = pd.DataFrame({"feature": X.columns, "importance": importance.importances_mean, "importance_std": importance.importances_std}).sort_values("importance", ascending=False)
    subgroup_rows = []
    test_evidence = X_test.assign(actual=y_test.to_numpy(), probability=probability)
    test_evidence["prediction"] = (probability >= 0.5).astype(int)
    test_evidence["age_group"] = pd.cut(test_evidence["age"], bins=[0, 34, 54, np.inf], labels=["18-34", "35-54", "55+"])
    for field in ["gender", "age_group"]:
        for value, subset in test_evidence.groupby(field, observed=True):
            subgroup_rows.append({"field": field, "group": str(value), "rows": int(len(subset)), "accuracy": float((subset["actual"] == subset["prediction"]).mean()), "labour_share": float(subset["actual"].mean())})
    subgroup = pd.DataFrame(subgroup_rows)
    comparison.to_csv(paths["tables"] / "model_comparison.csv", index=False)
    importance_table.to_csv(paths["tables"] / "permutation_importance.csv", index=False)
    subgroup.to_csv(paths["tables"] / "subgroup_sensitivity.csv", index=False)
    joblib.dump(calibrated, paths["models"] / "final_calibrated_model.joblib")

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    ordered = comparison.sort_values("cv_roc_auc_mean")
    axes[0, 0].barh(ordered["model"], ordered["cv_roc_auc_mean"], color="#2f6690")
    axes[0, 0].axvline(0.5, linestyle="--", color="#d1495b"); axes[0, 0].set(title="Training CV model selection", xlabel="Mean ROC-AUC", xlim=(0.45, 1))
    matrix = np.array([[test_metrics["true_negatives"], test_metrics["false_positives"]], [test_metrics["false_negatives"], test_metrics["true_positives"]]])
    axes[0, 1].imshow(matrix, cmap="Blues")
    for (row, col), value in np.ndenumerate(matrix): axes[0, 1].text(col, row, str(value), ha="center", va="center", fontsize=13)
    axes[0, 1].set(title="Untouched-test confusion matrix", xlabel="Predicted", ylabel="Actual", xticks=[0, 1], yticks=[0, 1])
    fraction, mean_prediction = calibration_curve(y_test, probability, n_bins=8, strategy="quantile")
    axes[1, 0].plot(mean_prediction, fraction, marker="o", color="#2f6690"); axes[1, 0].plot([0, 1], [0, 1], "--", color="#555555")
    axes[1, 0].set(title="Untouched-test calibration", xlabel="Predicted Labour probability", ylabel="Observed Labour share")
    top = importance_table.head(8).sort_values("importance")
    axes[1, 1].barh(top["feature"], top["importance"], color="#4f9d69"); axes[1, 1].set(title="Permutation importance", xlabel="Decrease in ROC-AUC")
    fig.tight_layout(); fig.savefig(paths["figures"] / "election_model_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"rows": int(len(raw)), "columns": int(raw.shape[1]), "missing_cells": int(raw.isna().sum().sum()), "duplicate_rows": int(raw.duplicated().sum()), "labour_share": float(y.mean())},
        "validation": {"training_rows": int(len(X_train)), "untouched_test_rows": int(len(X_test)), "selection": "5-fold stratified CV on training only", "selection_metric": "ROC-AUC", "random_seed": RANDOM_STATE},
        "candidate_models": comparison.to_dict(orient="records"), "selected_model": selected_name,
        "test_metrics": test_metrics, "top_permutation_features": importance_table.head(8).to_dict(orient="records"),
        "subgroup_sensitivity": subgroup.to_dict(orient="records"),
        "interpretation": "This is retrospective respondent classification, not vote-share estimation, polling, persuasion, or seat forecasting.",
        "responsible_use": "The undocumented sampling and weighting design prevents representative election inference or future-election claims.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
