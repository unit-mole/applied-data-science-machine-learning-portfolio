"""Auditable Online Retail RFM segmentation with stability and sensitivity checks."""

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
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, write_json

RANDOM_STATE = 42


def _segment_name(row: pd.Series, medians: pd.Series) -> str:
    recent = row["median_recency"] <= medians["median_recency"]
    frequent = row["median_frequency"] >= medians["median_frequency"]
    valuable = row["median_monetary"] >= medians["median_monetary"]
    if recent and frequent and valuable:
        return "High-value loyal customers"
    if not recent and frequent and valuable:
        return "Lapsed high-value customers"
    if recent and not frequent:
        return "Recent low-frequency customers"
    return "Occasional low-value customers"


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    raw = pd.read_excel(ROOT / "data" / "online_retail.xlsx")
    data_quality_table(raw).to_csv(paths["tables"] / "data_quality.csv", index=False)
    data = raw.copy()
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    cancelled = data["InvoiceNo"].astype(str).str.startswith("C")
    duplicate = data.duplicated()
    valid_mask = data["CustomerID"].notna() & data["InvoiceDate"].notna() & data["Quantity"].gt(0) & data["UnitPrice"].gt(0) & ~cancelled & ~duplicate
    valid = data.loc[valid_mask].copy()
    valid["Revenue"] = valid["Quantity"] * valid["UnitPrice"]
    snapshot = valid["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = valid.groupby("CustomerID").agg(
        recency=("InvoiceDate", lambda values: int((snapshot - values.max()).days)),
        frequency=("InvoiceNo", "nunique"), monetary=("Revenue", "sum"),
    )
    transformed = np.log1p(rfm)
    scaler = StandardScaler().fit(transformed)
    scaled = scaler.transform(transformed)
    evaluation_rows = []
    models: dict[int, KMeans] = {}
    rng = np.random.default_rng(RANDOM_STATE)
    sample_index = rng.choice(len(rfm), size=min(4000, len(rfm)), replace=False)
    for clusters in range(2, 8):
        model = KMeans(n_clusters=clusters, n_init=30, random_state=RANDOM_STATE).fit(scaled)
        models[clusters] = model
        reference = model.labels_
        stability = []
        for seed in [7, 19, 31, 53, 79]:
            alternate = KMeans(n_clusters=clusters, n_init=10, random_state=seed).fit_predict(scaled)
            stability.append(adjusted_rand_score(reference, alternate))
        evaluation_rows.append({
            "method": "kmeans", "clusters": clusters,
            "silhouette": float(silhouette_score(scaled[sample_index], reference[sample_index])),
            "davies_bouldin": float(davies_bouldin_score(scaled, reference)),
            "calinski_harabasz": float(calinski_harabasz_score(scaled, reference)),
            "mean_seed_stability_ari": float(np.mean(stability)),
            "smallest_cluster_share": float(pd.Series(reference).value_counts(normalize=True).min()),
        })
        mixture = GaussianMixture(n_components=clusters, covariance_type="full", n_init=3, random_state=RANDOM_STATE).fit(scaled)
        mixture_labels = mixture.predict(scaled)
        evaluation_rows.append({
            "method": "gaussian_mixture", "clusters": clusters,
            "silhouette": float(silhouette_score(scaled[sample_index], mixture_labels[sample_index])),
            "davies_bouldin": float(davies_bouldin_score(scaled, mixture_labels)),
            "calinski_harabasz": float(calinski_harabasz_score(scaled, mixture_labels)),
            "mean_seed_stability_ari": None,
            "smallest_cluster_share": float(pd.Series(mixture_labels).value_counts(normalize=True).min()),
        })
    evaluation = pd.DataFrame(evaluation_rows)
    eligible = evaluation[(evaluation["method"] == "kmeans") & (evaluation["smallest_cluster_share"] >= 0.05) & (evaluation["mean_seed_stability_ari"] >= 0.80)].copy()
    eligible["silhouette_rank"] = eligible["silhouette"].rank(ascending=False)
    eligible["davies_rank"] = eligible["davies_bouldin"].rank(ascending=True)
    eligible["stability_rank"] = eligible["mean_seed_stability_ari"].rank(ascending=False)
    eligible["composite_rank"] = eligible[["silhouette_rank", "davies_rank", "stability_rank"]].mean(axis=1)
    selected_k = int(eligible.sort_values(["composite_rank", "clusters"]).iloc[0]["clusters"])
    labels = models[selected_k].labels_
    rfm["cluster"] = labels
    profiles = rfm.groupby("cluster").agg(customers=("recency", "size"), median_recency=("recency", "median"), median_frequency=("frequency", "median"), median_monetary=("monetary", "median"), total_revenue=("monetary", "sum"))
    profiles["portfolio_share"] = profiles["customers"] / len(rfm)
    medians = profiles[["median_recency", "median_frequency", "median_monetary"]].median()
    profiles["segment_name"] = profiles.apply(_segment_name, axis=1, medians=medians)

    winsorized = rfm[["recency", "frequency", "monetary"]].clip(upper=rfm[["recency", "frequency", "monetary"]].quantile(0.99), axis=1)
    winsor_scaled = StandardScaler().fit_transform(np.log1p(winsorized))
    winsor_labels = KMeans(n_clusters=selected_k, n_init=30, random_state=RANDOM_STATE).fit_predict(winsor_scaled)
    outlier_sensitivity_ari = float(adjusted_rand_score(labels, winsor_labels))
    reduced = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(scaled)

    evaluation.to_csv(paths["tables"] / "cluster_model_selection.csv", index=False)
    profiles.to_csv(paths["tables"] / "segment_profiles.csv")
    rfm.assign(segment_name=pd.Series(labels, index=rfm.index).map(profiles["segment_name"])).to_csv(paths["tables"] / "customer_segments.csv")
    cleaning = pd.DataFrame({"reason": ["source rows", "exact duplicates", "cancelled invoices", "missing customer ID", "nonpositive quantity", "nonpositive price", "valid purchase rows"], "rows": [len(raw), duplicate.sum(), cancelled.sum(), raw["CustomerID"].isna().sum(), raw["Quantity"].le(0).sum(), raw["UnitPrice"].le(0).sum(), len(valid)]})
    cleaning.to_csv(paths["tables"] / "cleaning_funnel.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    kmeans_eval = evaluation[evaluation["method"] == "kmeans"]
    axes[0, 0].plot(kmeans_eval["clusters"], kmeans_eval["silhouette"], marker="o", label="silhouette")
    axes[0, 0].plot(kmeans_eval["clusters"], kmeans_eval["mean_seed_stability_ari"], marker="o", label="seed stability ARI")
    axes[0, 0].axvline(selected_k, color="#d1495b", linestyle="--"); axes[0, 0].set(title="Cluster-count evidence", xlabel="Clusters", ylabel="Score", ylim=(0, 1)); axes[0, 0].legend()
    scatter = axes[0, 1].scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="tab10", s=13, alpha=0.55)
    axes[0, 1].set(title="RFM customers projected with PCA", xlabel="Principal component 1", ylabel="Principal component 2"); axes[0, 1].legend(*scatter.legend_elements(), title="Cluster")
    profile_plot = profiles[["median_recency", "median_frequency", "median_monetary"]].copy()
    profile_plot = (profile_plot - profile_plot.mean()) / profile_plot.std(ddof=0)
    image = axes[1, 0].imshow(profile_plot, cmap="RdYlGn", aspect="auto")
    axes[1, 0].set(title="Standardized segment profile", yticks=range(len(profile_plot)), yticklabels=profiles["segment_name"], xticks=range(3), xticklabels=["Recency", "Frequency", "Monetary"])
    fig.colorbar(image, ax=axes[1, 0], fraction=0.046)
    axes[1, 1].barh(cleaning["reason"], cleaning["rows"], color="#2f6690"); axes[1, 1].set(title="Transaction cleaning evidence", xlabel="Rows (overlapping exclusion reasons)")
    fig.tight_layout(); fig.savefig(paths["figures"] / "online_retail_segmentation_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    selected_row = evaluation[(evaluation["method"] == "kmeans") & (evaluation["clusters"] == selected_k)].iloc[0]
    results = {
        "status": "passed",
        "data_quality": {"source_rows": int(len(raw)), "valid_purchase_rows": int(len(valid)), "exact_duplicates_excluded": int(duplicate.sum()), "cancelled_rows": int(cancelled.sum()), "rows_missing_customer_id": int(raw["CustomerID"].isna().sum()), "customers_segmented": int(len(rfm)), "snapshot_date": str(snapshot.date())},
        "feature_engineering": {"unit": "CustomerID", "features": ["recency_days", "unique_purchase_invoices", "net_positive_purchase_revenue"], "transformation": "log1p then standardization"},
        "model_selection": {"methods": ["K-means", "Gaussian mixture"], "candidate_clusters": list(range(2, 8)), "selection_rule": "composite rank among K-means candidates with >=5% smallest segment and >=0.80 seed ARI", "selected_clusters": selected_k, "selected_silhouette": float(selected_row["silhouette"]), "selected_davies_bouldin": float(selected_row["davies_bouldin"]), "selected_calinski_harabasz": float(selected_row["calinski_harabasz"]), "selected_seed_stability_ari": float(selected_row["mean_seed_stability_ari"])},
        "outlier_sensitivity": {"winsorized_at_99_percent_ari_vs_primary": outlier_sensitivity_ari},
        "segment_profiles": profiles.reset_index().round(3).to_dict(orient="records"),
        "responsible_use": "Segments describe historical purchasing behavior and must not support discriminatory pricing, credit decisions, or sensitive profiling.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
