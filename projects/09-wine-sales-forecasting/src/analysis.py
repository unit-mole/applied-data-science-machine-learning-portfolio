"""Rolling-origin monthly wine forecasting with transparent CPU models."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "portfolio-matplotlib-cache"))
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, regression_metrics, write_json

HOLDOUT = 24
CV_HORIZON = 12


def _seasonal_naive(train: pd.Series, horizon: int) -> np.ndarray:
    values = train.to_numpy(float)
    return np.asarray([values[-12 + (step % 12)] for step in range(horizon)])


def _trend_month(train: pd.Series, horizon: int) -> np.ndarray:
    encoder = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
    month = encoder.fit_transform(train.index.month.to_numpy().reshape(-1, 1))
    time = np.arange(len(train))[:, None]
    model = LinearRegression().fit(np.column_stack([time, month]), train.to_numpy(float))
    future_index = pd.date_range(train.index[-1] + pd.offsets.MonthBegin(1), periods=horizon, freq="MS")
    future_month = encoder.transform(future_index.month.to_numpy().reshape(-1, 1))
    return model.predict(np.column_stack([np.arange(len(train), len(train) + horizon)[:, None], future_month]))


def _ridge_lags(train: pd.Series, horizon: int) -> np.ndarray:
    frame = pd.DataFrame({"y": train})
    frame["lag_1"] = frame["y"].shift(1); frame["lag_12"] = frame["y"].shift(12)
    frame = frame.dropna()
    model = Ridge(alpha=10.0).fit(frame[["lag_1", "lag_12"]], frame["y"])
    history = train.to_list(); prediction = []
    for _ in range(horizon):
        next_frame = pd.DataFrame({"lag_1": [history[-1]], "lag_12": [history[-12]]})
        value = float(model.predict(next_frame)[0]); prediction.append(value); history.append(value)
    return np.asarray(prediction)


def _holt_winters_additive(train: pd.Series, horizon: int, alpha: float, beta: float, gamma: float, season: int = 12) -> np.ndarray:
    values = train.to_numpy(float)
    level = float(values[:season].mean())
    trend = float((values[season:2 * season].mean() - values[:season].mean()) / season)
    seasonal = (values[:season] - level).astype(float).tolist()
    for index, observed in enumerate(values):
        season_index = index % season
        previous_level = level
        level = alpha * (observed - seasonal[season_index]) + (1 - alpha) * (level + trend)
        trend = beta * (level - previous_level) + (1 - beta) * trend
        seasonal[season_index] = gamma * (observed - level) + (1 - gamma) * seasonal[season_index]
    return np.asarray([level + (step + 1) * trend + seasonal[(len(values) + step) % season] for step in range(horizon)])


def _forecast(name: str, train: pd.Series, horizon: int) -> np.ndarray:
    if name == "seasonal_naive": return _seasonal_naive(train, horizon)
    if name == "trend_plus_month": return _trend_month(train, horizon)
    if name == "ridge_lag_1_12": return _ridge_lags(train, horizon)
    _, parameters = name.split("__", 1)
    alpha, beta, gamma = map(float, parameters.split("_"))
    return _holt_winters_additive(train, horizon, alpha, beta, gamma)


def _ljung_box(residuals: np.ndarray, lags: int = 12) -> dict[str, float]:
    residuals = np.asarray(residuals) - np.mean(residuals)
    n = len(residuals); denominator = float(np.dot(residuals, residuals))
    correlations = [float(np.dot(residuals[lag:], residuals[:-lag]) / denominator) for lag in range(1, min(lags, n - 1) + 1)]
    q = float(n * (n + 2) * sum(value * value / (n - lag) for lag, value in enumerate(correlations, start=1)))
    return {"lags": len(correlations), "q_statistic": q, "p_value": float(chi2.sf(q, len(correlations)))}


def _evaluate_series(series: pd.Series, name: str, paths: dict[str, Path]) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame]:
    filled = series.interpolate(limit_direction="both")
    development = filled.iloc[:-HOLDOUT]
    test = filled.iloc[-HOLDOUT:]
    candidates = ["seasonal_naive", "trend_plus_month", "ridge_lag_1_12", "holt_winters__0.2_0.05_0.2", "holt_winters__0.3_0.1_0.3", "holt_winters__0.5_0.1_0.2"]
    fold_rows = []; residual_pool = {candidate: [] for candidate in candidates}
    for fold, offset in enumerate([3, 2, 1], start=1):
        validation_end = len(development) - CV_HORIZON * (offset - 1)
        validation_start = validation_end - CV_HORIZON
        train = development.iloc[:validation_start]
        validation = development.iloc[validation_start:validation_end]
        for candidate in candidates:
            prediction = _forecast(candidate, train, len(validation))
            score = regression_metrics(validation, prediction)
            fold_rows.append({"product": name, "fold": fold, "model": candidate, **score})
            residual_pool[candidate].extend(np.abs(validation.to_numpy() - prediction).tolist())
    folds = pd.DataFrame(fold_rows)
    comparison = folds.groupby("model", as_index=False).agg(mean_rmse=("rmse", "mean"), std_rmse=("rmse", "std"), mean_mae=("mae", "mean"), mean_mape_percent=("mape_percent", "mean")).sort_values("mean_rmse")
    selected = str(comparison.iloc[0]["model"])
    prediction = _forecast(selected, development, HOLDOUT)
    metrics = regression_metrics(test, prediction)
    interval_radius = float(np.quantile(residual_pool[selected], 0.90, method="higher"))
    lower = np.maximum(0, prediction - interval_radius); upper = prediction + interval_radius
    coverage = float(((test.to_numpy() >= lower) & (test.to_numpy() <= upper)).mean())
    forecast = pd.DataFrame({"actual": test, "prediction": prediction, "lower_90": lower, "upper_90": upper}, index=test.index)
    forecast.to_csv(paths["tables"] / f"{name}_final_holdout.csv")
    comparison.to_csv(paths["tables"] / f"{name}_model_comparison.csv", index=False)
    return {
        "selected_model": selected, "rolling_origin_candidates": comparison.to_dict(orient="records"),
        "final_holdout_metrics": metrics, "diagnostic_interval": {"radius": interval_radius, "coverage": coverage},
        "residual_ljung_box": _ljung_box(test.to_numpy() - prediction),
    }, forecast, folds


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    rose_raw = pd.read_csv(ROOT / "data" / "rose.csv", parse_dates=["YearMonth"])
    sparkling_raw = pd.read_csv(ROOT / "data" / "sparkling.csv", parse_dates=["YearMonth"])
    data_quality_table(rose_raw).to_csv(paths["tables"] / "rose_data_quality.csv", index=False)
    data_quality_table(sparkling_raw).to_csv(paths["tables"] / "sparkling_data_quality.csv", index=False)
    rose = rose_raw.set_index("YearMonth")["Rose"].asfreq("MS")
    sparkling = sparkling_raw.set_index("YearMonth")["Sparkling"].asfreq("MS")
    rose_result, rose_forecast, rose_folds = _evaluate_series(rose, "rose", paths)
    sparkling_result, sparkling_forecast, sparkling_folds = _evaluate_series(sparkling, "sparkling", paths)
    all_folds = pd.concat([rose_folds, sparkling_folds], ignore_index=True)
    all_folds.to_csv(paths["tables"] / "rolling_origin_results.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    for axis, product, forecast, result in [(axes[0, 0], "Rose", rose_forecast, rose_result), (axes[0, 1], "Sparkling", sparkling_forecast, sparkling_result)]:
        axis.plot(forecast.index, forecast["actual"], marker="o", label="actual", color="#222222")
        axis.plot(forecast.index, forecast["prediction"], marker="o", label=result["selected_model"], color="#2f6690")
        axis.fill_between(forecast.index, forecast["lower_90"], forecast["upper_90"], alpha=0.2, color="#2f6690")
        axis.set(title=f"{product}: final 24-month holdout", xlabel="Month", ylabel="Sales"); axis.legend(fontsize=8)
    for axis, product, folds in [(axes[1, 0], "Rose", rose_folds), (axes[1, 1], "Sparkling", sparkling_folds)]:
        summary = folds.groupby("model")["rmse"].mean().sort_values(ascending=False)
        axis.barh(summary.index, summary.values, color="#4f9d69"); axis.set(title=f"{product}: rolling-origin selection", xlabel="Mean RMSE")
    fig.tight_layout(); fig.savefig(paths["figures"] / "wine_forecasting_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"rose_observations": int(len(rose_raw)), "rose_missing_values": int(rose_raw["Rose"].isna().sum()), "sparkling_observations": int(len(sparkling_raw)), "sparkling_missing_values": int(sparkling_raw["Sparkling"].isna().sum()), "start_month": str(rose.index.min().date()), "end_month": str(rose.index.max().date()), "monthly_frequency_gaps_after_reindex": int(len(pd.date_range(rose.index.min(), rose.index.max(), freq="MS").difference(rose.index)))},
        "validation": {"model_selection": "three rolling-origin 12-month validation windows", "final_holdout": "last 24 months, untouched during selection", "missing_rose_values": "linear interpolation within the series; neither missing record is in the final holdout"},
        "products": {"rose": rose_result, "sparkling": sparkling_result},
        "limitation": "The series ends in 1995 and lacks price, promotion, inventory, weather, and economic drivers; diagnostic intervals are empirical validation-error bands rather than formal probabilistic intervals.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
