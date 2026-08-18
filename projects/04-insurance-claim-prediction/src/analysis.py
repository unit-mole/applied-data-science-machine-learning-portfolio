"""Leakage-safe insurance claim classification with calibration and threshold analysis."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import joblib
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "portfolio-matplotlib-cache"))
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score, balanced_accuracy_score, brier_score_loss,
    confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import (
    RandomizedSearchCV, StratifiedKFold, cross_val_predict, cross_validate,
    train_test_split,
)
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "insurance_claims.csv"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
TABLES = REPORTS / "tables"
MODELS = ROOT / "models"
RANDOM_STATE = 42


def _metrics(y_true: pd.Series, probability: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    prediction = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, prediction, labels=[0, 1]).ravel()
    return {
        "roc_auc": float(roc_auc_score(y_true, probability)),
        "pr_auc": float(average_precision_score(y_true, probability)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, prediction)),
        "precision": float(precision_score(y_true, prediction, zero_division=0)),
        "recall_sensitivity": float(recall_score(y_true, prediction, zero_division=0)),
        "specificity": float(tn / (tn + fp)) if tn + fp else 0.0,
        "f1": float(f1_score(y_true, prediction, zero_division=0)),
        "brier_score": float(brier_score_loss(y_true, probability)),
        "true_negatives": int(tn), "false_positives": int(fp),
        "false_negatives": int(fn), "true_positives": int(tp),
    }


def _pipeline(model: object, numeric: list[str], categorical: list[str]) -> Pipeline:
    preprocessing = ColumnTransformer(
        [
            ("numeric", StandardScaler(), numeric),
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical),
        ],
        verbose_feature_names_out=False,
    )
    return Pipeline([("preprocess", preprocessing), ("model", model)])


def run_analysis() -> dict[str, object]:
    """Execute model selection on training data and evaluate once on held-out data."""
    for directory in (REPORTS, FIGURES, TABLES, MODELS):
        directory.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(DATA)
    duplicate_rows = int(raw.duplicated().sum())
    data = raw.drop_duplicates().reset_index(drop=True)
    y = data.pop("Claimed").str.strip().str.lower().map({"no": 0, "yes": 1}).astype(int)
    X = data.copy()
    numeric = X.select_dtypes(include=np.number).columns.tolist()
    categorical = X.columns.difference(numeric).tolist()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE
    )
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
    candidates = {
        "dummy_prevalence": DummyClassifier(strategy="prior"),
        "logistic_regression": LogisticRegression(max_iter=1500, class_weight="balanced", random_state=RANDOM_STATE),
        "decision_tree": DecisionTreeClassifier(max_depth=5, min_samples_leaf=15, class_weight="balanced", random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=250, min_samples_leaf=4, class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE),
        "gradient_boosting": GradientBoostingClassifier(n_estimators=150, learning_rate=0.04, max_depth=2, random_state=RANDOM_STATE),
        "mlp": MLPClassifier(hidden_layer_sizes=(24,), alpha=0.01, early_stopping=True, max_iter=500, random_state=RANDOM_STATE),
    }
    scoring = {"roc_auc": "roc_auc", "pr_auc": "average_precision", "balanced_accuracy": "balanced_accuracy"}
    model_rows: list[dict[str, object]] = []
    fitted_candidates: dict[str, Pipeline] = {}
    for name, estimator in candidates.items():
        pipeline = _pipeline(estimator, numeric, categorical)
        scores = cross_validate(pipeline, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)
        fitted_candidates[name] = pipeline
        model_rows.append({
            "model": name,
            "cv_pr_auc_mean": float(scores["test_pr_auc"].mean()),
            "cv_pr_auc_std": float(scores["test_pr_auc"].std(ddof=1)),
            "cv_roc_auc_mean": float(scores["test_roc_auc"].mean()),
            "cv_balanced_accuracy_mean": float(scores["test_balanced_accuracy"].mean()),
            "selection_stage": "candidate",
        })

    forest_search = RandomizedSearchCV(
        _pipeline(RandomForestClassifier(class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE), numeric, categorical),
        {
            "model__n_estimators": [200, 350, 500], "model__max_depth": [None, 6, 10],
            "model__min_samples_leaf": [2, 4, 8], "model__max_features": ["sqrt", 0.7],
        },
        n_iter=8, scoring="average_precision", cv=cv, random_state=RANDOM_STATE, n_jobs=-1,
    )
    forest_search.fit(X_train, y_train)
    fitted_candidates["random_forest_tuned"] = forest_search.best_estimator_
    model_rows.append({
        "model": "random_forest_tuned", "cv_pr_auc_mean": float(forest_search.best_score_),
        "cv_pr_auc_std": np.nan, "cv_roc_auc_mean": np.nan,
        "cv_balanced_accuracy_mean": np.nan, "selection_stage": "randomized_search_8_candidates",
    })
    comparison = pd.DataFrame(model_rows).sort_values("cv_pr_auc_mean", ascending=False).reset_index(drop=True)
    selected_name = str(comparison.loc[0, "model"])
    selected = fitted_candidates[selected_name]

    oof_probability = cross_val_predict(clone(selected), X_train, y_train, cv=cv, method="predict_proba", n_jobs=-1)[:, 1]
    threshold_rows = []
    for threshold in np.arange(0.10, 0.81, 0.05):
        row = _metrics(y_train, oof_probability, float(threshold))
        threshold_rows.append({"threshold": float(threshold), "precision": row["precision"], "recall": row["recall_sensitivity"], "f1": row["f1"]})
    thresholds = pd.DataFrame(threshold_rows)
    selected_threshold = float(thresholds.loc[thresholds["f1"].idxmax(), "threshold"])

    calibrated = CalibratedClassifierCV(estimator=clone(selected), method="sigmoid", cv=cv)
    calibrated.fit(X_train, y_train)
    test_probability = calibrated.predict_proba(X_test)[:, 1]
    test_default = _metrics(y_test, test_probability, 0.5)
    test_selected = _metrics(y_test, test_probability, selected_threshold)
    importance = permutation_importance(
        calibrated, X_test, y_test, scoring="average_precision", n_repeats=12,
        random_state=RANDOM_STATE, n_jobs=-1,
    )
    importance_table = pd.DataFrame({
        "feature": X.columns, "pr_auc_importance_mean": importance.importances_mean,
        "importance_std": importance.importances_std,
    }).sort_values("pr_auc_importance_mean", ascending=False)
    quality = pd.DataFrame({
        "column": raw.columns, "dtype": raw.dtypes.astype(str).values,
        "missing_count": raw.isna().sum().values,
        "missing_percent": (raw.isna().mean() * 100).round(2).values,
        "unique_values": raw.nunique(dropna=False).values,
    })
    comparison.to_csv(TABLES / "model_comparison.csv", index=False)
    thresholds.to_csv(TABLES / "threshold_analysis.csv", index=False)
    importance_table.to_csv(TABLES / "permutation_importance.csv", index=False)
    quality.to_csv(TABLES / "data_quality.csv", index=False)
    joblib.dump(calibrated, MODELS / "final_calibrated_model.joblib")

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    plot_data = comparison.sort_values("cv_pr_auc_mean")
    axes[0, 0].barh(plot_data["model"], plot_data["cv_pr_auc_mean"], color="#2f6690")
    axes[0, 0].axvline(float(y_train.mean()), color="#d1495b", linestyle="--", label="claim prevalence")
    axes[0, 0].set(title="Training CV model selection", xlabel="Mean PR-AUC", xlim=(0, 1)); axes[0, 0].legend()
    matrix = np.array([[test_selected["true_negatives"], test_selected["false_positives"]], [test_selected["false_negatives"], test_selected["true_positives"]]])
    image = axes[0, 1].imshow(matrix, cmap="Blues")
    for (row, col), value in np.ndenumerate(matrix):
        axes[0, 1].text(col, row, str(value), ha="center", va="center", fontsize=13)
    axes[0, 1].set(title=f"Untouched test confusion matrix (threshold={selected_threshold:.2f})", xlabel="Predicted", ylabel="Actual", xticks=[0, 1], yticks=[0, 1])
    fig.colorbar(image, ax=axes[0, 1], fraction=0.046)
    fraction, mean_predicted = calibration_curve(y_test, test_probability, n_bins=8, strategy="quantile")
    axes[1, 0].plot(mean_predicted, fraction, marker="o", color="#2f6690", label=selected_name)
    axes[1, 0].plot([0, 1], [0, 1], linestyle="--", color="#555555")
    axes[1, 0].set(title="Test-set calibration", xlabel="Mean predicted probability", ylabel="Observed claim rate"); axes[1, 0].legend()
    top = importance_table.head(8).sort_values("pr_auc_importance_mean")
    axes[1, 1].barh(top["feature"], top["pr_auc_importance_mean"], color="#4f9d69")
    axes[1, 1].set(title="Permutation importance on untouched test set", xlabel="Decrease in PR-AUC")
    fig.tight_layout(); fig.savefig(FIGURES / "insurance_model_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"raw_rows": int(len(raw)), "exact_duplicates_removed": duplicate_rows, "modeling_rows": int(len(X)), "missing_cells": int(raw.isna().sum().sum()), "claim_prevalence": float(y.mean())},
        "validation": {"train_rows": int(len(X_train)), "untouched_test_rows": int(len(X_test)), "test_fraction": 0.25, "selection_cv": "4-fold stratified CV on training data only", "optimization_metric": "average precision (PR-AUC)", "random_seed": RANDOM_STATE},
        "candidate_models": comparison.replace({np.nan: None}).to_dict(orient="records"),
        "tuning": {"model": "random_forest", "search": "8-candidate randomized search", "best_parameters": forest_search.best_params_},
        "selected_model": selected_name,
        "selected_threshold_from_training_oof": selected_threshold,
        "test_metrics_default_threshold": test_default,
        "test_metrics_selected_threshold": test_selected,
        "top_permutation_features": importance_table.head(10).to_dict(orient="records"),
        "decision_note": "False negatives represent missed claimed policies; threshold selection maximized training out-of-fold F1 and was fixed before test evaluation.",
        "responsible_use": "Educational model only; never use it to approve, deny, price, or investigate an insurance claim.",
    }
    (REPORTS / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
