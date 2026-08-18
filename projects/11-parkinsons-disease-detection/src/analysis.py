"""Participant-safe Parkinson's voice classification for educational evaluation."""

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
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.svm import SVC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import binary_metrics, classification_pipeline, data_quality_table, ensure_output_dirs, write_json

RANDOM_STATE = 42


def _participant_table(groups: pd.Series, truth: pd.Series, probability: np.ndarray) -> pd.DataFrame:
    frame = pd.DataFrame({"participant": groups.to_numpy(), "actual": truth.to_numpy(), "probability": probability})
    return frame.groupby("participant", as_index=False).agg(actual=("actual", "first"), probability=("probability", "mean"), recordings=("actual", "size"))


def _bootstrap_interval(participants: pd.DataFrame, metric: str, iterations: int = 1000) -> list[float]:
    rng = np.random.default_rng(RANDOM_STATE)
    values = []
    for _ in range(iterations):
        sampled = participants.iloc[rng.integers(0, len(participants), len(participants))]
        if sampled["actual"].nunique() < 2:
            continue
        values.append(float(binary_metrics(sampled["actual"], sampled["probability"])[metric]))
    return [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))] if values else [float("nan"), float("nan")]


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_csv(ROOT / "data" / "parkinsons.csv")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    groups = raw["name"].str.rsplit("_", n=1).str[0]
    participant_labels = pd.DataFrame({"participant": groups, "status": raw["status"]}).groupby("participant", as_index=False)["status"].first()
    train_people, test_people = train_test_split(participant_labels, test_size=0.25, stratify=participant_labels["status"], random_state=RANDOM_STATE)
    train_mask = groups.isin(train_people["participant"])
    test_mask = groups.isin(test_people["participant"])
    X = raw.drop(columns=["name", "status"])
    y = raw["status"].astype(int)
    X_train, X_test = X.loc[train_mask].reset_index(drop=True), X.loc[test_mask].reset_index(drop=True)
    y_train, y_test = y.loc[train_mask].reset_index(drop=True), y.loc[test_mask].reset_index(drop=True)
    groups_train, groups_test = groups.loc[train_mask].reset_index(drop=True), groups.loc[test_mask].reset_index(drop=True)
    cv = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
    estimators = {
        "dummy_prevalence": DummyClassifier(strategy="prior"),
        "logistic_regression": LogisticRegression(max_iter=2000, class_weight="balanced", C=0.3, random_state=RANDOM_STATE),
        "support_vector_machine": SVC(C=1.0, kernel="rbf", class_weight="balanced", probability=True, random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=400, min_samples_leaf=3, class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE),
        "gradient_boosting": GradientBoostingClassifier(n_estimators=120, learning_rate=0.04, max_depth=2, random_state=RANDOM_STATE),
    }
    models = {name: classification_pipeline(estimator, X) for name, estimator in estimators.items()}
    cv_rows = []
    for name, model in models.items():
        fold_metrics = []
        for fold, (fit_index, validation_index) in enumerate(cv.split(X_train, y_train, groups_train), start=1):
            fitted = clone(model).fit(X_train.iloc[fit_index], y_train.iloc[fit_index])
            probability = fitted.predict_proba(X_train.iloc[validation_index])[:, 1]
            participant = _participant_table(groups_train.iloc[validation_index], y_train.iloc[validation_index], probability)
            score = binary_metrics(participant["actual"], participant["probability"])
            fold_metrics.append({"fold": fold, **score})
        fold_frame = pd.DataFrame(fold_metrics)
        cv_rows.append({
            "model": name, "participant_cv_roc_auc_mean": float(fold_frame["roc_auc"].mean()),
            "participant_cv_roc_auc_std": float(fold_frame["roc_auc"].std(ddof=1)),
            "participant_cv_balanced_accuracy_mean": float(fold_frame["balanced_accuracy"].mean()),
            "participant_cv_recall_mean": float(fold_frame["recall_sensitivity"].mean()),
        })
    comparison = pd.DataFrame(cv_rows).sort_values("participant_cv_roc_auc_mean", ascending=False).reset_index(drop=True)
    selected_name = str(comparison.loc[0, "model"])
    final_model = clone(models[selected_name]).fit(X_train, y_train)
    probability = final_model.predict_proba(X_test)[:, 1]
    recording_metrics = binary_metrics(y_test, probability)
    participant_test = _participant_table(groups_test, y_test, probability)
    participant_metrics = binary_metrics(participant_test["actual"], participant_test["probability"])
    confidence_intervals = {
        "participant_roc_auc_95_percent_bootstrap": _bootstrap_interval(participant_test, "roc_auc"),
        "participant_balanced_accuracy_95_percent_bootstrap": _bootstrap_interval(participant_test, "balanced_accuracy"),
        "participant_recall_95_percent_bootstrap": _bootstrap_interval(participant_test, "recall_sensitivity"),
    }
    importance = permutation_importance(final_model, X_test, y_test, scoring="roc_auc", n_repeats=20, random_state=RANDOM_STATE, n_jobs=-1)
    importance_table = pd.DataFrame({"feature": X.columns, "importance": importance.importances_mean, "importance_std": importance.importances_std}).sort_values("importance", ascending=False)
    comparison.to_csv(paths["tables"] / "participant_grouped_cv.csv", index=False)
    participant_test.to_csv(paths["tables"] / "held_out_participant_predictions.csv", index=False)
    importance_table.to_csv(paths["tables"] / "permutation_importance.csv", index=False)
    joblib.dump(final_model, paths["models"] / "educational_voice_classifier.joblib")

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    ordered = comparison.sort_values("participant_cv_roc_auc_mean")
    axes[0, 0].barh(ordered["model"], ordered["participant_cv_roc_auc_mean"], color="#2f6690"); axes[0, 0].set(title="Participant-grouped CV selection", xlabel="Mean participant ROC-AUC", xlim=(0.4, 1))
    matrix = np.array([[participant_metrics["true_negatives"], participant_metrics["false_positives"]], [participant_metrics["false_negatives"], participant_metrics["true_positives"]]])
    axes[0, 1].imshow(matrix, cmap="Blues")
    for (row, col), value in np.ndenumerate(matrix): axes[0, 1].text(col, row, str(value), ha="center", va="center", fontsize=13)
    axes[0, 1].set(title="Held-out participant confusion matrix", xlabel="Predicted", ylabel="Actual", xticks=[0, 1], yticks=[0, 1])
    colors = participant_test["actual"].map({0: "#4f9d69", 1: "#d1495b"})
    axes[1, 0].scatter(range(len(participant_test)), participant_test["probability"], c=colors, s=70)
    axes[1, 0].axhline(0.5, color="#555555", linestyle="--"); axes[1, 0].set(title="Held-out participant probabilities", xlabel="Held-out participant", ylabel="Predicted probability", ylim=(0, 1))
    top = importance_table.head(10).sort_values("importance")
    axes[1, 1].barh(top["feature"], top["importance"], color="#e9a03b"); axes[1, 1].set(title="Recording-level permutation importance", xlabel="Decrease in ROC-AUC")
    fig.tight_layout(); fig.savefig(paths["figures"] / "participant_safe_model_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"recordings": int(len(raw)), "participants": int(groups.nunique()), "features": int(X.shape[1]), "missing_cells": int(raw.isna().sum().sum()), "positive_participants": int(participant_labels["status"].sum())},
        "validation": {"train_participants": int(train_people.shape[0]), "held_out_participants": int(test_people.shape[0]), "same_participant_in_train_and_test": bool(set(train_people["participant"]) & set(test_people["participant"])), "model_selection": "4-fold StratifiedGroupKFold on training participants", "random_seed": RANDOM_STATE},
        "candidate_models": comparison.to_dict(orient="records"), "selected_model": selected_name,
        "recording_level_test_metrics": recording_metrics, "participant_level_test_metrics": participant_metrics,
        "participant_bootstrap_intervals": confidence_intervals,
        "held_out_false_negative_participants": int(participant_metrics["false_negatives"]),
        "top_permutation_features": importance_table.head(10).to_dict(orient="records"),
        "responsible_use": "Educational evaluation only—not a diagnostic, screening, monitoring, or treatment system. The eight-person holdout and absent external validation preclude clinical use.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
