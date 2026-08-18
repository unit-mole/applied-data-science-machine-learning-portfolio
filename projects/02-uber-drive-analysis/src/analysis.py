"""Decision-oriented exploratory analysis of a personal Uber trip log."""

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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, write_json


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_csv(ROOT / "data" / "uber_drives.csv")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    data = raw.rename(columns={column: column.rstrip("*").strip().lower().replace(" ", "_") for column in raw.columns})
    data["start_date"] = pd.to_datetime(data["start_date"], format="mixed", errors="coerce")
    data["end_date"] = pd.to_datetime(data["end_date"], format="mixed", errors="coerce")
    data["miles"] = pd.to_numeric(data["miles"], errors="coerce")
    invalid_source_rows = int((data["start_date"].isna() | data["end_date"].isna() | data["miles"].isna()).sum())
    duplicate_rows = int(data.duplicated().sum())
    trips = data.drop_duplicates().dropna(subset=["start_date", "end_date", "miles"]).copy()
    trips["purpose"] = trips["purpose"].fillna("Unknown").str.strip()
    trips["category"] = trips["category"].fillna("Unknown").str.strip()
    trips["duration_minutes"] = (trips["end_date"] - trips["start_date"]).dt.total_seconds() / 60
    trips["average_speed_mph"] = trips["miles"] / (trips["duration_minutes"] / 60)
    impossible_duration = trips["duration_minutes"].le(0)
    suspicious_speed = trips["average_speed_mph"].gt(100) | trips["average_speed_mph"].lt(0)
    trips.loc[impossible_duration, "average_speed_mph"] = np.nan
    trips["month"] = trips["start_date"].dt.to_period("M").astype(str)
    trips["weekday"] = pd.Categorical(trips["start_date"].dt.day_name(), categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True)
    trips["hour"] = trips["start_date"].dt.hour
    trips["daypart"] = pd.cut(trips["hour"], bins=[-1, 5, 11, 16, 20, 23], labels=["Overnight", "Morning", "Afternoon", "Evening", "Late night"])
    trips["route"] = trips["start"].astype(str) + " → " + trips["stop"].astype(str)
    q1, q3 = trips["miles"].quantile([0.25, 0.75]); outlier_limit = q3 + 1.5 * (q3 - q1)
    outlier_trips = trips[trips["miles"] > outlier_limit].sort_values("miles", ascending=False)
    monthly = trips.groupby("month", as_index=False).agg(trips=("miles", "size"), miles=("miles", "sum"), median_miles=("miles", "median"))
    weekday = trips.groupby("weekday", observed=True).agg(trips=("miles", "size"), miles=("miles", "sum"), median_duration=("duration_minutes", "median"))
    purpose = trips.groupby("purpose").agg(trips=("miles", "size"), miles=("miles", "sum"), median_miles=("miles", "median")).sort_values("miles", ascending=False)
    routes = trips.groupby("route").agg(trips=("miles", "size"), miles=("miles", "sum")).sort_values(["trips", "miles"], ascending=False).head(15)
    known_purpose = purpose.drop(index="Unknown", errors="ignore")
    known_routes = trips[~trips["route"].str.contains("Unknown Location", regex=False)].groupby("route").agg(trips=("miles", "size"), miles=("miles", "sum")).sort_values(["trips", "miles"], ascending=False)
    monthly.to_csv(paths["tables"] / "monthly_trip_summary.csv", index=False); weekday.to_csv(paths["tables"] / "weekday_summary.csv")
    purpose.to_csv(paths["tables"] / "purpose_summary.csv"); routes.to_csv(paths["tables"] / "top_routes.csv"); outlier_trips.to_csv(paths["tables"] / "distance_outliers.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes[0, 0].plot(monthly["month"], monthly["miles"], marker="o", color="#2f6690"); axes[0, 0].set(title="Recorded mileage by month", xlabel="Month", ylabel="Miles"); axes[0, 0].tick_params(axis="x", rotation=45)
    purpose.head(10).sort_values("miles")["miles"].plot.barh(ax=axes[0, 1], color="#4f9d69"); axes[0, 1].set(title="Top purposes by total mileage", xlabel="Miles", ylabel="Purpose")
    weekday["miles"].plot.bar(ax=axes[1, 0], color="#e9a03b"); axes[1, 0].set(title="Mileage by weekday", xlabel="Weekday", ylabel="Miles"); axes[1, 0].tick_params(axis="x", rotation=35)
    axes[1, 1].hist(trips["miles"], bins=35, color="#7d5ba6", alpha=0.8); axes[1, 1].axvline(outlier_limit, color="#d1495b", linestyle="--", label=f"IQR outlier limit {outlier_limit:.1f}")
    axes[1, 1].set(title="Trip-distance distribution", xlabel="Miles", ylabel="Trips"); axes[1, 1].legend()
    fig.tight_layout(); fig.savefig(paths["figures"] / "uber_trip_behavior_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"source_rows": int(len(raw)), "valid_trip_rows": int(len(trips)), "invalid_or_summary_rows_removed": invalid_source_rows, "exact_duplicates_removed": duplicate_rows, "missing_purpose_rows_retained_as_unknown": int(raw["PURPOSE*"].isna().sum()), "nonpositive_duration_rows": int(impossible_duration.sum()), "suspicious_speed_rows_over_100_mph": int(suspicious_speed.sum())},
        "scope": {"first_trip": str(trips["start_date"].min()), "last_trip": str(trips["start_date"].max()), "observed_months": int(trips["month"].nunique()), "unit": "trip"},
        "trip_summary": {"total_trips": int(len(trips)), "total_miles": float(trips["miles"].sum()), "median_trip_miles": float(trips["miles"].median()), "median_duration_minutes": float(trips["duration_minutes"].median()), "business_mileage_share": float(trips.loc[trips["category"].str.lower() == "business", "miles"].sum() / trips["miles"].sum()), "distance_outlier_trips": int(len(outlier_trips))},
        "leading_patterns": {"highest_mileage_month": str(monthly.loc[monthly["miles"].idxmax(), "month"]), "highest_mileage_weekday": str(weekday["miles"].idxmax()), "highest_mileage_known_purpose": str(known_purpose.index[0]), "most_frequent_known_route": str(known_routes.index[0])},
        "recommendations": ["Maintain explicit purpose capture because missing purpose limits reimbursement and productivity analysis.", "Review high-mileage outliers individually before expense or utilization decisions.", "Use recurring route and weekday concentrations for scheduling—not for employee surveillance."],
        "limitation": "This is one personal log over a limited period; location and purpose data are sensitive and findings do not generalize to platform-wide demand.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
