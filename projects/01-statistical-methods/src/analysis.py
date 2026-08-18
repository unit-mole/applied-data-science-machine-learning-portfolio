"""Decision-oriented inference for wholesale, survey, and shingle case studies."""

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
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from portfolio_lib import data_quality_table, ensure_output_dirs, write_json


def _holm(values: list[float]) -> list[float]:
    order = np.argsort(values); adjusted = np.empty(len(values)); running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(values) - rank) * values[index])); adjusted[index] = running
    return adjusted.tolist()


def _cohen_d(first: np.ndarray, second: np.ndarray) -> float:
    pooled = np.sqrt(((len(first) - 1) * first.var(ddof=1) + (len(second) - 1) * second.var(ddof=1)) / (len(first) + len(second) - 2))
    return float((first.mean() - second.mean()) / pooled) if pooled else 0.0


def _one_sample(values: pd.Series, limit: float) -> dict[str, object]:
    clean = values.dropna().to_numpy(float); mean = clean.mean(); sem = stats.sem(clean)
    t_result = stats.ttest_1samp(clean, popmean=limit, alternative="less")
    confidence = stats.t.interval(0.95, len(clean) - 1, loc=mean, scale=sem)
    centered = clean - limit
    nonzero = centered[centered != 0]
    wilcoxon = stats.wilcoxon(nonzero, alternative="less")
    return {"n": int(len(clean)), "sample_mean": float(mean), "sample_std": float(clean.std(ddof=1)), "mean_95_percent_ci": [float(confidence[0]), float(confidence[1])], "one_sided_t_statistic": float(t_result.statistic), "one_sided_t_p_value": float(t_result.pvalue), "standardized_effect_vs_limit": float((mean - limit) / clean.std(ddof=1)), "wilcoxon_signed_rank_p_value": float(wilcoxon.pvalue)}


def run_analysis() -> dict[str, object]:
    paths = ensure_output_dirs(ROOT)
    wholesale = pd.read_csv(ROOT / "data" / "wholesale_customers.csv")
    survey = pd.read_csv(ROOT / "data" / "university_survey.csv")
    shingles = pd.read_csv(ROOT / "data" / "shingles.csv")
    for name, frame in [("wholesale", wholesale), ("survey", survey), ("shingles", shingles)]:
        data_quality_table(frame).to_csv(paths["tables"] / f"{name}_data_quality.csv", index=False)
    spend = ["Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicatessen"]
    wholesale = wholesale.copy(); wholesale["total_spend"] = wholesale[spend].sum(axis=1)
    by_channel = wholesale.groupby("Channel")["total_spend"].agg(["count", "mean", "median", "sum"])
    by_region = wholesale.groupby("Region")["total_spend"].agg(["count", "mean", "median", "sum"])
    cv = (wholesale[spend].std(ddof=1) / wholesale[spend].mean()).sort_values(ascending=False)
    channel_values = {name: group for name, group in wholesale.groupby("Channel")}
    channel_names = sorted(channel_values)
    channel_tests = []
    for category in spend + ["total_spend"]:
        first = channel_values[channel_names[0]][category].to_numpy(float); second = channel_values[channel_names[1]][category].to_numpy(float)
        welch = stats.ttest_ind(first, second, equal_var=False); mann = stats.mannwhitneyu(first, second, alternative="two-sided")
        channel_tests.append({"measure": category, "channel_1": str(channel_names[0]), "channel_2": str(channel_names[1]), "mean_difference": float(first.mean() - second.mean()), "cohen_d": _cohen_d(first, second), "welch_p_value": float(welch.pvalue), "mann_whitney_p_value": float(mann.pvalue)})
    channel_tests = pd.DataFrame(channel_tests); channel_tests["holm_adjusted_welch_p"] = _holm(channel_tests["welch_p_value"].tolist())
    contingency = pd.crosstab(survey["Gender"], survey["Major"])
    chi_square, chi_p, degrees, expected = stats.chi2_contingency(contingency)
    cramers_v = float(np.sqrt(chi_square / (contingency.to_numpy().sum() * min(contingency.shape[0] - 1, contingency.shape[1] - 1))))
    shingle_tests = {column: _one_sample(shingles[column], 0.35) for column in ["A", "B"]}
    equality = stats.ttest_ind(shingles["A"].dropna(), shingles["B"].dropna(), equal_var=False)
    by_channel.to_csv(paths["tables"] / "wholesale_channel_summary.csv"); by_region.to_csv(paths["tables"] / "wholesale_region_summary.csv")
    channel_tests.to_csv(paths["tables"] / "wholesale_channel_tests.csv", index=False); contingency.to_csv(paths["tables"] / "survey_gender_major_contingency.csv")

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    wholesale.boxplot(column="total_spend", by="Channel", ax=axes[0, 0]); axes[0, 0].set_yscale("log"); axes[0, 0].set(title="Wholesale customer spend by channel", xlabel="Channel", ylabel="Total spend (log scale)"); axes[0, 0].figure.suptitle("")
    cv.sort_values().plot.barh(ax=axes[0, 1], color="#4f9d69"); axes[0, 1].set(title="Relative category variability", xlabel="Coefficient of variation")
    image = axes[1, 0].imshow(contingency, cmap="Blues", aspect="auto")
    axes[1, 0].set(title="Survey respondents: gender by major", xlabel="Major", ylabel="Gender", xticks=range(len(contingency.columns)), xticklabels=contingency.columns, yticks=range(len(contingency.index)), yticklabels=contingency.index)
    for (row, col), value in np.ndenumerate(contingency.to_numpy()): axes[1, 0].text(col, row, str(value), ha="center", va="center")
    fig.colorbar(image, ax=axes[1, 0], fraction=0.046)
    summary = shingles[["A", "B"]].agg(["mean", "sem"]).T
    axes[1, 1].bar(summary.index, summary["mean"], yerr=1.96 * summary["sem"], capsize=6, color=["#7d5ba6", "#d1495b"]); axes[1, 1].axhline(0.35, color="#333333", linestyle="--", label="0.35 limit")
    axes[1, 1].set(title="Shingle moisture means with approximate 95% CI", xlabel="Shingle type", ylabel="Moisture"); axes[1, 1].legend()
    fig.tight_layout(); fig.savefig(paths["figures"] / "statistical_decision_evidence.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    results = {
        "status": "passed",
        "data_quality": {"wholesale_rows": int(len(wholesale)), "survey_rows": int(len(survey)), "shingle_rows": int(len(shingles)), "total_missing_cells": int(wholesale.isna().sum().sum() + survey.isna().sum().sum() + shingles.isna().sum().sum()), "duplicate_rows_across_inputs": int(wholesale.duplicated().sum() + survey.duplicated().sum() + shingles.duplicated().sum())},
        "wholesale": {"highest_total_spend_channel": str(by_channel["sum"].idxmax()), "highest_total_spend_region": str(by_region["sum"].idxmax()), "most_variable_category_by_cv": str(cv.index[0]), "category_channel_tests": channel_tests.to_dict(orient="records")},
        "survey_gender_major": {"chi_square": float(chi_square), "p_value": float(chi_p), "degrees_of_freedom": int(degrees), "cramers_v": cramers_v, "expected_cells_below_5": int((expected < 5).sum()), "assumption_warning": bool((expected < 5).mean() > 0.20)},
        "shingles": {"specification_limit": 0.35, "one_sample_results": shingle_tests, "welch_a_vs_b": {"t_statistic": float(equality.statistic), "p_value": float(equality.pvalue), "cohen_d": _cohen_d(shingles["A"].dropna().to_numpy(), shingles["B"].dropna().to_numpy())}},
        "limitations": "The survey and shingle collection designs are undocumented; inferential results apply only under independence and sampling assumptions that cannot be fully verified.",
    }
    write_json(paths["reports"] / "metrics.json", results)
    return results


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2))
