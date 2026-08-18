"""Robust salary group inference and interpretable college-admissions PCA."""

from __future__ import annotations

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
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, write_json


def _eta_squared(groups: list[np.ndarray]) -> float:
    values = np.concatenate(groups); grand = values.mean()
    between = sum(len(group) * (group.mean() - grand) ** 2 for group in groups)
    return float(between / ((values - grand) ** 2).sum())


def _cohen_d(first: np.ndarray, second: np.ndarray) -> float:
    pooled = np.sqrt(((len(first) - 1) * first.var(ddof=1) + (len(second) - 1) * second.var(ddof=1)) / (len(first) + len(second) - 2))
    return float((first.mean() - second.mean()) / pooled) if pooled else 0.0


def _holm(values: list[float]) -> list[float]:
    order = np.argsort(values); adjusted = np.empty(len(values)); running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(values) - rank) * values[index])); adjusted[index] = running
    return adjusted.tolist()


def _pairwise(frame: pd.DataFrame, field: str) -> pd.DataFrame:
    rows = []
    for first, second in itertools.combinations(sorted(frame[field].unique()), 2):
        a = frame.loc[frame[field] == first, "Salary"].to_numpy(float); b = frame.loc[frame[field] == second, "Salary"].to_numpy(float)
        test = stats.ttest_ind(a, b, equal_var=False)
        rows.append({"field": field, "group_1": str(first), "group_2": str(second), "mean_difference": float(a.mean() - b.mean()), "cohen_d": _cohen_d(a, b), "welch_p_value": float(test.pvalue)})
    result = pd.DataFrame(rows); result["holm_adjusted_p_value"] = _holm(result["welch_p_value"].tolist())
    return result


def _design_matrix(data: pd.DataFrame, interaction: bool) -> np.ndarray:
    education = pd.get_dummies(data["Education"], drop_first=True, dtype=float)
    occupation = pd.get_dummies(data["Occupation"], drop_first=True, dtype=float)
    blocks = [np.ones((len(data), 1)), education.to_numpy(), occupation.to_numpy()]
    if interaction:
        blocks.extend((education[column].to_numpy() * occupation[other].to_numpy())[:, None] for column in education for other in occupation)
    return np.column_stack(blocks)


def _nested_interaction(y: np.ndarray, reduced: np.ndarray, full: np.ndarray) -> dict[str, float | int]:
    def rss(matrix: np.ndarray) -> tuple[float, int]:
        residual = y - matrix @ np.linalg.lstsq(matrix, y, rcond=None)[0]
        return float(np.dot(residual, residual)), int(np.linalg.matrix_rank(matrix))
    reduced_rss, reduced_rank = rss(reduced); full_rss, full_rank = rss(full)
    numerator_df = full_rank - reduced_rank; denominator_df = len(y) - full_rank
    statistic = ((reduced_rss - full_rss) / numerator_df) / (full_rss / denominator_df)
    return {"f_statistic": float(statistic), "p_value": float(stats.f.sf(statistic, numerator_df, denominator_df)), "numerator_df": numerator_df, "denominator_df": denominator_df}


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    salary = pd.read_csv(ROOT / "data" / "salary_data.csv")
    college = pd.read_csv(ROOT / "data" / "college_admissions.csv")
    data_quality_table(salary).to_csv(paths["tables"] / "salary_data_quality.csv", index=False)
    data_quality_table(college).to_csv(paths["tables"] / "college_data_quality.csv", index=False)
    inference = {}; pairwise_frames = []
    for field in ["Education", "Occupation"]:
        groups = [group["Salary"].to_numpy(float) for _, group in salary.groupby(field)]
        classic = stats.f_oneway(*groups); welch = stats.f_oneway(*groups, equal_var=False); kruskal = stats.kruskal(*groups); levene = stats.levene(*groups, center="median")
        inference[field.lower()] = {"classic_anova_f": float(classic.statistic), "classic_anova_p": float(classic.pvalue), "welch_anova_f": float(welch.statistic), "welch_anova_p": float(welch.pvalue), "kruskal_h": float(kruskal.statistic), "kruskal_p": float(kruskal.pvalue), "levene_p": float(levene.pvalue), "eta_squared": _eta_squared(groups)}
        pairwise_frames.append(_pairwise(salary, field))
    pairwise = pd.concat(pairwise_frames, ignore_index=True)
    interaction = _nested_interaction(salary["Salary"].to_numpy(float), _design_matrix(salary, False), _design_matrix(salary, True))
    additive = _design_matrix(salary, False); residuals = salary["Salary"].to_numpy(float) - additive @ np.linalg.lstsq(additive, salary["Salary"].to_numpy(float), rcond=None)[0]
    residual_normality = stats.shapiro(residuals)

    features = college.drop(columns=["Names"])
    scaler = StandardScaler(); scaled = scaler.fit_transform(features)
    pca = PCA(random_state=42).fit(scaled); scores = pca.transform(scaled)
    cumulative = np.cumsum(pca.explained_variance_ratio_)
    components_80 = int(np.argmax(cumulative >= 0.80) + 1); components_90 = int(np.argmax(cumulative >= 0.90) + 1)
    loadings = pd.DataFrame(pca.components_.T, index=features.columns, columns=[f"PC{index + 1}" for index in range(len(features.columns))])
    top_loadings = []
    for component in ["PC1", "PC2", "PC3"]:
        for feature in loadings[component].abs().nlargest(5).index:
            top_loadings.append({"component": component, "feature": feature, "loading": float(loadings.loc[feature, component])})
    reconstructed = scores[:, :components_80] @ pca.components_[:components_80] + pca.mean_
    reconstruction_rmse = float(np.sqrt(np.mean((scaled - reconstructed) ** 2)))
    distance = np.sqrt((scores[:, :components_80] ** 2).sum(axis=1))
    outlier_count = int((distance > np.quantile(distance, 0.99)).sum())
    pairwise.to_csv(paths["tables"] / "salary_pairwise_holm.csv", index=False)
    loadings.to_csv(paths["tables"] / "pca_loadings.csv")
    pd.DataFrame(scores[:, :components_80], index=college["Names"], columns=[f"PC{i+1}" for i in range(components_80)]).to_csv(paths["tables"] / "college_component_scores.csv")

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    salary.boxplot(column="Salary", by="Education", ax=axes[0, 0]); axes[0, 0].set(title="Salary distribution by education", xlabel="Education", ylabel="Salary"); axes[0, 0].figure.suptitle("")
    salary.boxplot(column="Salary", by="Occupation", ax=axes[0, 1]); axes[0, 1].set(title="Salary distribution by occupation", xlabel="Occupation", ylabel="Salary"); axes[0, 1].figure.suptitle("")
    x = np.arange(1, len(cumulative) + 1); axes[1, 0].plot(x, pca.explained_variance_ratio_, marker="o", label="individual"); axes[1, 0].plot(x, cumulative, marker="o", label="cumulative")
    axes[1, 0].axhline(0.80, color="#d1495b", linestyle="--"); axes[1, 0].set(title="PCA explained variance", xlabel="Component", ylabel="Variance share", ylim=(0, 1.02)); axes[1, 0].legend()
    loading_plot = loadings[["PC1", "PC2"]].loc[loadings[["PC1", "PC2"]].abs().max(axis=1).nlargest(10).index]
    axes[1, 1].scatter(scores[:, 0], scores[:, 1], s=12, alpha=0.35, color="#2f6690")
    for feature, row in loading_plot.iterrows(): axes[1, 1].arrow(0, 0, row["PC1"] * 8, row["PC2"] * 8, color="#d1495b", alpha=0.6); axes[1, 1].text(row["PC1"] * 8.4, row["PC2"] * 8.4, feature, fontsize=7)
    axes[1, 1].set(title="College PCA score/loading map", xlabel="PC1", ylabel="PC2")
    fig.tight_layout(); fig.savefig(paths["figures"] / "anova_pca_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"salary_rows": int(len(salary)), "salary_groups": {"education": int(salary["Education"].nunique()), "occupation": int(salary["Occupation"].nunique())}, "college_rows": int(len(college)), "college_numeric_features": int(features.shape[1]), "missing_cells": int(salary.isna().sum().sum() + college.isna().sum().sum())},
        "salary_inference": {**inference, "education_occupation_interaction": interaction, "additive_model_residual_shapiro_p": float(residual_normality.pvalue), "pairwise_tests": pairwise.to_dict(orient="records")},
        "pca": {"standardized": True, "components_for_80_percent": components_80, "components_for_90_percent": components_90, "first_three_explained_variance": pca.explained_variance_ratio_[:3].tolist(), "reconstruction_rmse_at_80_percent_components": reconstruction_rmse, "top_loadings": top_loadings, "extreme_score_rows_above_99th_percentile": outlier_count},
        "limitation": "The salary sample has only 40 observational records; robust alternatives and corrected pairwise tests reduce but do not eliminate small-sample and design limitations.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
