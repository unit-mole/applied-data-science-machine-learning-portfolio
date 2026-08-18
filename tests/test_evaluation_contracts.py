"""Check leakage-sensitive evaluation claims recorded by the pipelines."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def metrics(slug: str) -> dict:
    return json.loads((ROOT / "projects" / slug / "reports" / "metrics.json").read_text(encoding="utf-8"))

class EvaluationContracts(unittest.TestCase):
    def test_participant_split_has_no_overlap(self) -> None:
        result = metrics("11-parkinsons-disease-detection")
        self.assertFalse(result["validation"]["same_participant_in_train_and_test"])
        self.assertGreater(result["validation"]["held_out_participants"], 0)

    def test_forecasts_have_temporal_holdouts(self) -> None:
        wine = metrics("09-wine-sales-forecasting")
        covid = metrics("13-covid-outbreak-prediction")
        self.assertIn("24 months", wine["validation"]["final_holdout"])
        self.assertLess(covid["validation"]["final_holdout_start"], covid["validation"]["final_holdout_end"])

    def test_cluster_projects_record_stability(self) -> None:
        retail = metrics("12-online-retail-segmentation")
        self.assertGreater(retail["model_selection"]["selected_seed_stability_ari"], 0.8)
        self.assertGreater(retail["outlier_sensitivity"]["winsorized_at_99_percent_ari_vs_primary"], 0.8)

if __name__ == "__main__":
    unittest.main()
