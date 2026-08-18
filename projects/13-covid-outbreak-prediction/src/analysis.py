"""Historical one-day-ahead COVID case modeling with rolling temporal validation."""

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
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, regression_metrics, write_json

RANDOM_STATE = 42
HORIZON_DAYS = 14


def _ridge_pipeline(numeric: list[str]) -> TransformedTargetRegressor:
    preprocess = ColumnTransformer([
        ("numeric", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("location", OneHotEncoder(handle_unknown="ignore"), ["location"]),
    ])
    return TransformedTargetRegressor(regressor=Pipeline([("preprocess", preprocess), ("model", Ridge(alpha=10.0))]), func=np.log1p, inverse_func=np.expm1)


def _boosting_pipeline(numeric: list[str]) -> TransformedTargetRegressor:
    return TransformedTargetRegressor(
        regressor=Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("model", HistGradientBoostingRegressor(max_iter=220, learning_rate=0.055, max_leaf_nodes=31, l2_regularization=2.0, random_state=RANDOM_STATE)),
        ]), func=np.log1p, inverse_func=np.expm1,
    )


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_csv(ROOT / "data" / "covid.csv")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    data = raw.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data[data["iso_code"].notna() & ~data["iso_code"].astype(str).str.startswith("OWID_")].sort_values(["location", "date"])
    negative_revisions = int(data["new_cases"].lt(0).sum())
    groups = data.groupby("location", group_keys=False)
    for lag in [1, 2, 3, 7, 14]:
        data[f"lag_{lag}"] = groups["new_cases"].shift(lag).clip(lower=0)
    data["rolling_7"] = groups["new_cases"].transform(lambda values: values.shift(1).clip(lower=0).rolling(7).mean())
    data["rolling_14"] = groups["new_cases"].transform(lambda values: values.shift(1).clip(lower=0).rolling(14).mean())
    data["total_cases_lag_1"] = groups["total_cases"].shift(1)
    data["day_index"] = (data["date"] - data["date"].min()).dt.days
    numeric = ["lag_1", "lag_2", "lag_3", "lag_7", "lag_14", "rolling_7", "rolling_14", "total_cases_lag_1", "population", "stringency_index", "day_index"]
    modeling = data.dropna(subset=["date", "new_cases", "lag_1", "lag_7", "rolling_7", "total_cases_lag_1"]).copy()
    modeling = modeling[modeling["new_cases"].ge(0)]
    final_date = modeling["date"].max()
    final_start = final_date - pd.Timedelta(days=HORIZON_DAYS - 1)
    validation_starts = [final_start - pd.Timedelta(days=HORIZON_DAYS * offset) for offset in [3, 2, 1]]
    models = {"ridge_country_lags": _ridge_pipeline(numeric), "hist_gradient_boosting_lags": _boosting_pipeline(numeric)}
    fold_rows = []
    residual_pool: dict[str, list[float]] = {name: [] for name in ["last_value", "rolling_7_baseline", *models]}
    for fold, start in enumerate(validation_starts, start=1):
        end = start + pd.Timedelta(days=HORIZON_DAYS - 1)
        train = modeling[modeling["date"] < start]
        validation = modeling[(modeling["date"] >= start) & (modeling["date"] <= end)]
        predictions = {
            "last_value": validation["lag_1"].to_numpy(),
            "rolling_7_baseline": validation["rolling_7"].to_numpy(),
        }
        for name, model in models.items():
            features = [*numeric, "location"] if name.startswith("ridge") else numeric
            model.fit(train[features], train["new_cases"])
            predictions[name] = np.clip(model.predict(validation[features]), 0, None)
        for name, prediction in predictions.items():
            score = regression_metrics(validation["new_cases"], prediction)
            fold_rows.append({"fold": fold, "start": str(start.date()), "end": str(end.date()), "model": name, "rows": int(len(validation)), **score})
            residual_pool[name].extend(np.abs(validation["new_cases"].to_numpy() - prediction).tolist())
    folds = pd.DataFrame(fold_rows)
    comparison = folds.groupby("model", as_index=False).agg(mean_rmse=("rmse", "mean"), std_rmse=("rmse", "std"), mean_mae=("mae", "mean"), mean_r_squared=("r_squared", "mean"))
    comparison = comparison.sort_values("mean_rmse").reset_index(drop=True)
    selected_name = str(comparison.loc[0, "model"])
    train = modeling[modeling["date"] < final_start]
    test = modeling[modeling["date"] >= final_start]
    if selected_name == "last_value":
        prediction = test["lag_1"].to_numpy()
    elif selected_name == "rolling_7_baseline":
        prediction = test["rolling_7"].to_numpy()
    else:
        selected = models[selected_name]
        features = [*numeric, "location"] if selected_name.startswith("ridge") else numeric
        selected.fit(train[features], train["new_cases"])
        prediction = np.clip(selected.predict(test[features]), 0, None)
        joblib.dump(selected, paths["models"] / "historical_next_day_model.joblib")
    test_metrics = regression_metrics(test["new_cases"], prediction)
    interval_radius = float(np.quantile(residual_pool[selected_name], 0.90, method="higher"))
    lower, upper = np.maximum(0, prediction - interval_radius), prediction + interval_radius
    interval_coverage = float(((test["new_cases"].to_numpy() >= lower) & (test["new_cases"].to_numpy() <= upper)).mean())
    country_error = pd.DataFrame({"location": test["location"], "actual": test["new_cases"], "prediction": prediction})
    country_error["absolute_error"] = (country_error["actual"] - country_error["prediction"]).abs()
    country_summary = country_error.groupby("location", as_index=False).agg(rows=("actual", "size"), actual_cases=("actual", "sum"), mae=("absolute_error", "mean")).sort_values("actual_cases", ascending=False)
    daily = pd.DataFrame({"date": test["date"], "actual": test["new_cases"], "prediction": prediction, "lower": lower, "upper": upper}).groupby("date", as_index=False).sum()
    folds.to_csv(paths["tables"] / "rolling_origin_results.csv", index=False)
    comparison.to_csv(paths["tables"] / "model_comparison.csv", index=False)
    country_summary.to_csv(paths["tables"] / "test_error_by_country.csv", index=False)
    daily.to_csv(paths["tables"] / "aggregated_test_forecast.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes[0, 0].plot(daily["date"], daily["actual"], marker="o", label="reported cases", color="#222222")
    axes[0, 0].plot(daily["date"], daily["prediction"], marker="o", label=selected_name, color="#2f6690")
    axes[0, 0].fill_between(daily["date"], daily["lower"], daily["upper"], alpha=0.18, color="#2f6690", label="aggregated diagnostic interval")
    axes[0, 0].set(title="Final chronological holdout: aggregated one-day-ahead cases", xlabel="Date", ylabel="Reported new cases"); axes[0, 0].legend()
    ordered = comparison.sort_values("mean_rmse", ascending=False)
    axes[0, 1].barh(ordered["model"], ordered["mean_rmse"], color="#2f6690"); axes[0, 1].set(title="Rolling-origin model selection", xlabel="Mean RMSE across three windows")
    for model, subset in folds.groupby("model"):
        axes[1, 0].plot(subset["fold"], subset["rmse"], marker="o", label=model)
    axes[1, 0].set(title="RMSE stability across forecast windows", xlabel="Validation window", ylabel="RMSE", xticks=[1, 2, 3]); axes[1, 0].legend(fontsize=8)
    top = country_summary.head(12).sort_values("mae")
    axes[1, 1].barh(top["location"], top["mae"], color="#d1495b"); axes[1, 1].set(title="Final-holdout error for highest-volume countries", xlabel="Mean absolute error")
    fig.tight_layout(); fig.savefig(paths["figures"] / "historical_covid_validation_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"source_rows": int(len(raw)), "source_locations": int(raw["location"].nunique()), "source_date_min": str(pd.to_datetime(raw["date"]).min().date()), "source_date_max": str(pd.to_datetime(raw["date"]).max().date()), "negative_case_revision_rows_excluded": negative_revisions, "modeling_rows": int(len(modeling)), "modeled_locations": int(modeling["location"].nunique())},
        "forecast_definition": {"target": "reported new cases for the current row using only prior-day and earlier features", "horizon": "one day ahead", "historical_cutoff": str(final_date.date())},
        "validation": {"selection": "three rolling-origin 14-day windows", "final_holdout_start": str(final_start.date()), "final_holdout_end": str(final_date.date()), "final_train_rows": int(len(train)), "final_test_rows": int(len(test)), "random_seed": RANDOM_STATE},
        "candidate_models": comparison.to_dict(orient="records"), "selected_model": selected_name, "final_test_metrics": test_metrics,
        "diagnostic_90_percent_interval": {"absolute_error_radius_from_validation": interval_radius, "final_test_coverage": interval_coverage},
        "highest_volume_country_errors": country_summary.head(12).to_dict(orient="records"),
        "responsible_use": "Historical educational analysis only. Early-pandemic reporting revisions, testing changes, policy shifts, and short coverage make it unsuitable for current forecasting, policy, or medical decisions.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
