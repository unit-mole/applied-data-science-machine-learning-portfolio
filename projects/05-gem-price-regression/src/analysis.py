"""Cross-validated gem-price regression with diagnostics and interval evidence."""

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
from scipy import stats
from sklearn.base import clone
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, regression_metrics, write_json

RANDOM_STATE = 42


def _pipeline(estimator: object, frame: pd.DataFrame) -> Pipeline:
    numeric = frame.select_dtypes(include=np.number).columns.tolist()
    categorical = frame.columns.difference(numeric).tolist()
    preprocessing = ColumnTransformer([
        ("numeric", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical),
    ], verbose_feature_names_out=False)
    return Pipeline([("preprocess", preprocessing), ("model", estimator)])


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_csv(ROOT / "data" / "cubic_zirconia.csv")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    identifier_columns = [column for column in raw.columns if column.lower().startswith("unnamed")]
    data = raw.drop(columns=identifier_columns)
    impossible_dimensions = int(((data[["x", "y", "z"]] <= 0).any(axis=1)).sum())
    y = data.pop("price").astype(float)
    X = data.copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=RANDOM_STATE)
    cv = KFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
    candidates = {
        "median_baseline": _pipeline(DummyRegressor(strategy="median"), X),
        "linear_regression": _pipeline(LinearRegression(), X),
        "log_target_ridge": TransformedTargetRegressor(regressor=_pipeline(Ridge(alpha=3.0), X), func=np.log1p, inverse_func=np.expm1),
        "random_forest": _pipeline(RandomForestRegressor(n_estimators=220, min_samples_leaf=3, max_features=0.8, n_jobs=-1, random_state=RANDOM_STATE), X),
        "hist_gradient_boosting": _pipeline(HistGradientBoostingRegressor(max_iter=260, learning_rate=0.06, max_leaf_nodes=31, l2_regularization=1.0, random_state=RANDOM_STATE), X),
    }
    rows = []
    for name, model in candidates.items():
        scores = cross_validate(model, X_train, y_train, cv=cv, scoring={"rmse": "neg_root_mean_squared_error", "mae": "neg_mean_absolute_error", "r2": "r2"}, n_jobs=-1)
        rows.append({
            "model": name, "cv_rmse_mean": float(-scores["test_rmse"].mean()), "cv_rmse_std": float(scores["test_rmse"].std(ddof=1)),
            "cv_mae_mean": float(-scores["test_mae"].mean()), "cv_r_squared_mean": float(scores["test_r2"].mean()),
        })
    comparison = pd.DataFrame(rows).sort_values("cv_rmse_mean").reset_index(drop=True)
    selected_name = str(comparison.loc[0, "model"])
    selected = candidates[selected_name]

    X_fit, X_calibration, y_fit, y_calibration = train_test_split(X_train, y_train, test_size=0.20, random_state=RANDOM_STATE)
    final_model = clone(selected).fit(X_fit, y_fit)
    calibration_prediction = final_model.predict(X_calibration)
    interval_radius = float(np.quantile(np.abs(y_calibration - calibration_prediction), 0.90, method="higher"))
    test_prediction = final_model.predict(X_test)
    test_metrics = regression_metrics(y_test, test_prediction)
    lower = np.maximum(0, test_prediction - interval_radius)
    upper = test_prediction + interval_radius
    interval_coverage = float(((y_test.to_numpy() >= lower) & (y_test.to_numpy() <= upper)).mean())
    residuals = y_test.to_numpy() - test_prediction
    residual_diagnostics = {
        "mean_residual": float(residuals.mean()), "residual_skewness": float(stats.skew(residuals)),
        "breusch_pagan_proxy_spearman_abs_residual_vs_prediction": float(stats.spearmanr(np.abs(residuals), test_prediction).statistic),
    }
    carat_band = pd.qcut(X_test["carat"], q=4, duplicates="drop")
    segment_rows = []
    for band in carat_band.cat.categories:
        mask = carat_band == band
        segment_rows.append({"carat_band": str(band), "rows": int(mask.sum()), **regression_metrics(y_test[mask], test_prediction[mask])})
    segment_error = pd.DataFrame(segment_rows)
    importance = permutation_importance(final_model, X_test, y_test, scoring="neg_root_mean_squared_error", n_repeats=10, random_state=RANDOM_STATE, n_jobs=-1)
    importance_table = pd.DataFrame({"feature": X.columns, "rmse_importance": importance.importances_mean, "importance_std": importance.importances_std}).sort_values("rmse_importance", ascending=False)

    comparison.to_csv(paths["tables"] / "model_comparison.csv", index=False)
    segment_error.to_csv(paths["tables"] / "error_by_carat_band.csv", index=False)
    importance_table.to_csv(paths["tables"] / "permutation_importance.csv", index=False)
    pd.DataFrame({"actual": y_test, "predicted": test_prediction, "interval_lower_90": lower, "interval_upper_90": upper, "residual": residuals}).to_csv(paths["tables"] / "test_predictions.csv", index=False)
    joblib.dump(final_model, paths["models"] / "final_price_model.joblib")

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    ordered = comparison.sort_values("cv_rmse_mean", ascending=False)
    axes[0, 0].barh(ordered["model"], ordered["cv_rmse_mean"], color="#2f6690"); axes[0, 0].set(title="Training CV model comparison", xlabel="RMSE (lower is better)")
    axes[0, 1].scatter(y_test, test_prediction, alpha=0.25, s=12, color="#2f6690"); bounds=[float(y_test.min()), float(y_test.max())]; axes[0, 1].plot(bounds, bounds, "--", color="#d1495b")
    axes[0, 1].set(title="Untouched test: actual versus predicted", xlabel="Actual price", ylabel="Predicted price")
    axes[1, 0].scatter(test_prediction, residuals, alpha=0.25, s=12, color="#4f9d69"); axes[1, 0].axhline(0, color="#d1495b", linestyle="--")
    axes[1, 0].set(title="Residual diagnostic", xlabel="Predicted price", ylabel="Actual − predicted")
    top = importance_table.head(8).sort_values("rmse_importance")
    axes[1, 1].barh(top["feature"], top["rmse_importance"], color="#e9a03b"); axes[1, 1].set(title="Permutation importance on test", xlabel="Increase in RMSE when permuted")
    fig.tight_layout(); fig.savefig(paths["figures"] / "gem_price_model_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"raw_rows": int(len(raw)), "columns": int(raw.shape[1]), "identifier_columns_excluded": identifier_columns, "missing_cells": int(raw.isna().sum().sum()), "duplicate_rows": int(raw.duplicated().sum()), "rows_with_nonpositive_dimensions": impossible_dimensions},
        "validation": {"training_rows": int(len(X_train)), "untouched_test_rows": int(len(X_test)), "model_selection": "4-fold shuffled CV on training only", "calibration_rows_for_interval": int(len(X_calibration)), "random_seed": RANDOM_STATE},
        "candidate_models": comparison.to_dict(orient="records"), "selected_model": selected_name,
        "test_metrics": test_metrics,
        "empirical_90_percent_interval": {"absolute_residual_radius": interval_radius, "test_coverage": interval_coverage, "method": "training calibration residual quantile; constant-width diagnostic interval"},
        "residual_diagnostics": residual_diagnostics, "error_by_carat_band": segment_error.to_dict(orient="records"),
        "top_permutation_features": importance_table.head(8).to_dict(orient="records"),
        "interpretation_caution": "Feature importance and fitted relationships are associative; the dataset does not support causal appraisal claims.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
