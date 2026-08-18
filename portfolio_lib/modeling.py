"""Reusable modeling and metric helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    average_precision_score, balanced_accuracy_score, brier_score_loss,
    confusion_matrix, f1_score, mean_absolute_error, mean_squared_error,
    precision_score, r2_score, recall_score, roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def binary_metrics(y_true: pd.Series | np.ndarray, probability: np.ndarray, threshold: float = 0.5) -> dict[str, float | int]:
    """Return imbalance-aware binary-classification metrics."""
    truth = np.asarray(y_true, dtype=int)
    prediction = (np.asarray(probability) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(truth, prediction, labels=[0, 1]).ravel()
    return {
        "roc_auc": float(roc_auc_score(truth, probability)),
        "pr_auc": float(average_precision_score(truth, probability)),
        "balanced_accuracy": float(balanced_accuracy_score(truth, prediction)),
        "precision": float(precision_score(truth, prediction, zero_division=0)),
        "recall_sensitivity": float(recall_score(truth, prediction, zero_division=0)),
        "specificity": float(tn / (tn + fp)) if tn + fp else 0.0,
        "f1": float(f1_score(truth, prediction, zero_division=0)),
        "brier_score": float(brier_score_loss(truth, probability)),
        "true_negatives": int(tn), "false_positives": int(fp),
        "false_negatives": int(fn), "true_positives": int(tp),
    }


def classification_pipeline(estimator: object, frame: pd.DataFrame, *, dense: bool = True) -> Pipeline:
    """Build a leakage-safe mixed-type classification pipeline."""
    numeric = frame.select_dtypes(include=np.number).columns.tolist()
    categorical = frame.columns.difference(numeric).tolist()
    preprocessor = ColumnTransformer(
        [
            ("numeric", StandardScaler(), numeric),
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=not dense), categorical),
        ],
        verbose_feature_names_out=False,
    )
    return Pipeline([("preprocess", preprocessor), ("model", estimator)])


def regression_metrics(y_true: pd.Series | np.ndarray, prediction: np.ndarray) -> dict[str, float]:
    """Return standard held-out regression metrics."""
    truth = np.asarray(y_true, dtype=float)
    predicted = np.asarray(prediction, dtype=float)
    nonzero = truth != 0
    return {
        "mae": float(mean_absolute_error(truth, predicted)),
        "rmse": float(np.sqrt(mean_squared_error(truth, predicted))),
        "r_squared": float(r2_score(truth, predicted)),
        "mape_percent": float(np.mean(np.abs((truth[nonzero] - predicted[nonzero]) / truth[nonzero])) * 100) if nonzero.any() else float("nan"),
    }

