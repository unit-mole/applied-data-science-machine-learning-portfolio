"""Fast portfolio contracts; no model retraining is performed here."""
from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "01-statistical-methods", "02-uber-drive-analysis", "03-anova-pca-analysis",
    "04-insurance-claim-prediction", "05-gem-price-regression", "06-holiday-package-prediction",
    "07-election-exit-poll-prediction", "08-presidential-speech-analysis", "09-wine-sales-forecasting",
    "10-marketing-retail-analysis", "11-parkinsons-disease-detection", "12-online-retail-segmentation",
    "13-covid-outbreak-prediction",
]

class PortfolioContracts(unittest.TestCase):
    def test_supported_runtime(self) -> None:
        self.assertIn(sys.version_info[:2], {(3, 12), (3, 13)})

    def test_exact_project_set(self) -> None:
        actual = sorted(path.name for path in (ROOT / "projects").iterdir() if path.is_dir())
        self.assertEqual(actual, EXPECTED)

    def test_recorded_evidence(self) -> None:
        for slug in EXPECTED:
            project = ROOT / "projects" / slug
            metrics = json.loads((project / "reports" / "metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(metrics.get("status"), "passed", slug)
            self.assertTrue(list((project / "reports" / "figures").glob("*.png")), slug)
            self.assertTrue(list((project / "reports" / "tables").glob("*.csv")), slug)

    def test_notebooks_are_substantive_and_executed(self) -> None:
        for slug in EXPECTED:
            path = ROOT / "projects" / slug / "notebooks" / "01_end_to_end_analysis.ipynb"
            notebook = json.loads(path.read_text(encoding="utf-8"))
            code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
            self.assertGreaterEqual(len(notebook["cells"]), 30, slug)
            self.assertGreaterEqual(len(code), 9, slug)
            self.assertTrue(all(cell["execution_count"] is not None for cell in code), slug)
            self.assertGreaterEqual(sum(bool(cell["outputs"]) for cell in code), 8, slug)
            self.assertFalse(any(o.get("output_type") == "error" for c in code for o in c["outputs"]), slug)

if __name__ == "__main__":
    unittest.main()
