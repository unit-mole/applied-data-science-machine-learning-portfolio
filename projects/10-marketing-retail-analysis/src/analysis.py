"""Cafe revenue, basket, daypart, and menu-item segmentation analysis."""

from __future__ import annotations

import collections
import itertools
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "portfolio-matplotlib-cache"))
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, write_json

RANDOM_STATE = 42


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_excel(ROOT / "data" / "cafe_transactions.xlsx")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    data = raw.rename(columns=lambda value: value.strip().replace(" ", "_"))
    duplicates = int(data.duplicated().sum()); data = data.drop_duplicates().copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Category"] = data["Category"].astype(str).str.strip().replace({"LIQUOR ": "LIQUOR"})
    time_text = data["Time"].astype(str)
    data["hour"] = pd.to_datetime(time_text, format="%H:%M:%S", errors="coerce").dt.hour
    data["daypart"] = pd.cut(data["hour"], bins=[-1, 5, 10, 15, 20, 23], labels=["Overnight", "Breakfast", "Lunch", "Evening", "Late night"])
    data["recorded_revenue"] = pd.to_numeric(data["Total"], errors="coerce")
    valid = data.dropna(subset=["Date", "Bill_Number", "Item_Desc", "recorded_revenue"]).copy()
    valid = valid[(valid["Quantity"] > 0) & (valid["recorded_revenue"] >= 0)]
    valid["month"] = valid["Date"].dt.to_period("M").astype(str)
    valid["weekday"] = pd.Categorical(valid["Date"].dt.day_name(), categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True)
    bills = valid.groupby("Bill_Number").agg(order_revenue=("recorded_revenue", "sum"), line_items=("Item_Desc", "size"), distinct_items=("Item_Desc", "nunique"), units=("Quantity", "sum"), date=("Date", "first"), daypart=("daypart", "first"))
    monthly = valid.groupby("month", as_index=False).agg(revenue=("recorded_revenue", "sum"), bills=("Bill_Number", "nunique"), units=("Quantity", "sum"))
    monthly["average_order_value"] = monthly["revenue"] / monthly["bills"]
    category = valid.groupby("Category").agg(revenue=("recorded_revenue", "sum"), bills=("Bill_Number", "nunique"), units=("Quantity", "sum")).sort_values("revenue", ascending=False)
    daypart = valid.groupby("daypart", observed=True).agg(revenue=("recorded_revenue", "sum"), bills=("Bill_Number", "nunique")).sort_values("revenue", ascending=False)

    basket_counter: collections.Counter[tuple[str, str]] = collections.Counter(); item_bill_counter: collections.Counter[str] = collections.Counter()
    for items in valid.groupby("Bill_Number")["Item_Desc"].agg(lambda values: sorted(set(values))):
        item_bill_counter.update(items)
        basket_counter.update(itertools.combinations(items, 2))
    total_bills = len(bills); pair_rows = []
    for (first, second), count in basket_counter.most_common(100):
        support = count / total_bills; first_support = item_bill_counter[first] / total_bills; second_support = item_bill_counter[second] / total_bills
        pair_rows.append({"item_1": first, "item_2": second, "joint_bills": count, "support": support, "confidence_1_to_2": support / first_support, "confidence_2_to_1": support / second_support, "lift": support / (first_support * second_support)})
    pairs = pd.DataFrame(pair_rows).query("joint_bills >= 20").sort_values(["lift", "joint_bills"], ascending=False)

    items = valid.groupby("Item_Desc").agg(revenue=("recorded_revenue", "sum"), units=("Quantity", "sum"), bills=("Bill_Number", "nunique"), median_rate=("Rate", "median"), median_line_total=("recorded_revenue", "median"))
    scaled = StandardScaler().fit_transform(np.log1p(items))
    cluster_rows = []; models = {}
    for clusters in range(2, 7):
        model = KMeans(n_clusters=clusters, n_init=30, random_state=RANDOM_STATE).fit(scaled); models[clusters] = model
        stability = [adjusted_rand_score(model.labels_, KMeans(n_clusters=clusters, n_init=10, random_state=seed).fit_predict(scaled)) for seed in [7, 19, 31, 53]]
        cluster_rows.append({"clusters": clusters, "silhouette": float(silhouette_score(scaled, model.labels_)), "davies_bouldin": float(davies_bouldin_score(scaled, model.labels_)), "mean_seed_stability_ari": float(np.mean(stability)), "smallest_cluster_share": float(pd.Series(model.labels_).value_counts(normalize=True).min())})
    cluster_evaluation = pd.DataFrame(cluster_rows); eligible = cluster_evaluation[cluster_evaluation["smallest_cluster_share"] >= 0.05]
    selected_k = int(eligible.sort_values(["silhouette", "mean_seed_stability_ari"], ascending=False).iloc[0]["clusters"])
    items["cluster"] = models[selected_k].labels_
    profiles = items.groupby("cluster").agg(items=("revenue", "size"), median_revenue=("revenue", "median"), median_units=("units", "median"), median_bills=("bills", "median"), median_rate=("median_rate", "median"))
    monthly.to_csv(paths["tables"] / "monthly_business_summary.csv", index=False); category.to_csv(paths["tables"] / "category_summary.csv"); daypart.to_csv(paths["tables"] / "daypart_summary.csv")
    pairs.to_csv(paths["tables"] / "basket_item_pairs.csv", index=False); cluster_evaluation.to_csv(paths["tables"] / "menu_cluster_selection.csv", index=False); profiles.to_csv(paths["tables"] / "menu_cluster_profiles.csv"); items.to_csv(paths["tables"] / "menu_item_segments.csv")

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes[0, 0].plot(monthly["month"], monthly["revenue"], marker="o", color="#2f6690"); axes[0, 0].set(title="Recorded revenue by month", xlabel="Month", ylabel="Recorded revenue"); axes[0, 0].tick_params(axis="x", rotation=45)
    category.head(10).sort_values("revenue")["revenue"].plot.barh(ax=axes[0, 1], color="#4f9d69"); axes[0, 1].set(title="Category contribution", xlabel="Recorded revenue", ylabel="Category")
    axes[1, 0].plot(cluster_evaluation["clusters"], cluster_evaluation["silhouette"], marker="o", label="silhouette"); axes[1, 0].plot(cluster_evaluation["clusters"], cluster_evaluation["mean_seed_stability_ari"], marker="o", label="stability ARI"); axes[1, 0].axvline(selected_k, color="#d1495b", linestyle="--"); axes[1, 0].set(title="Menu-item cluster evidence", xlabel="Clusters", ylabel="Score", ylim=(0, 1)); axes[1, 0].legend()
    top_pairs = pairs.sort_values("joint_bills", ascending=False).head(12).copy(); top_pairs["pair"] = top_pairs["item_1"].str.slice(0, 18) + " + " + top_pairs["item_2"].str.slice(0, 18)
    axes[1, 1].barh(top_pairs["pair"][::-1], top_pairs["joint_bills"][::-1], color="#e9a03b"); axes[1, 1].set(title="Frequent co-purchased item pairs", xlabel="Bills containing both items")
    fig.tight_layout(); fig.savefig(paths["figures"] / "cafe_business_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    selected_row = cluster_evaluation.loc[cluster_evaluation["clusters"] == selected_k].iloc[0]
    results = {
        "status": "passed",
        "data_quality": {"source_rows": int(len(raw)), "exact_duplicates_removed": duplicates, "valid_rows": int(len(valid)), "invalid_rows_removed": int(len(data) - len(valid)), "distinct_bills": int(len(bills)), "distinct_items": int(valid["Item_Desc"].nunique()), "date_min": str(valid["Date"].min().date()), "date_max": str(valid["Date"].max().date())},
        "business_summary": {"recorded_revenue": float(valid["recorded_revenue"].sum()), "average_order_value": float(bills["order_revenue"].mean()), "median_order_value": float(bills["order_revenue"].median()), "highest_revenue_category": str(category.index[0]), "highest_revenue_daypart": str(daypart.index[0]), "top_items_by_revenue": items["revenue"].nlargest(10).to_dict()},
        "basket_analysis": {"method": "bill-level pair co-occurrence", "minimum_joint_bills": 20, "top_pairs_by_lift": pairs.head(10).to_dict(orient="records"), "caution": "Association does not establish promotion lift; frequent items can dominate support."},
        "menu_item_segmentation": {"features": list(items.columns.drop("cluster")), "candidate_clusters": list(range(2, 7)), "selected_clusters": selected_k, "selected_silhouette": float(selected_row["silhouette"]), "selected_stability_ari": float(selected_row["mean_seed_stability_ari"]), "profiles": profiles.reset_index().to_dict(orient="records")},
        "limitation": "There is no customer identifier, so customer-level RFM, retention, and lifetime-value claims are not possible from this dataset.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
