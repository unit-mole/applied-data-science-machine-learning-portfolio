"""Validate structure, syntax, notebook evidence, links, paths, and result contracts."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = [
    "01-statistical-methods", "02-uber-drive-analysis", "03-anova-pca-analysis",
    "04-insurance-claim-prediction", "05-gem-price-regression", "06-holiday-package-prediction",
    "07-election-exit-poll-prediction", "08-presidential-speech-analysis", "09-wine-sales-forecasting",
    "10-marketing-retail-analysis", "11-parkinsons-disease-detection", "12-online-retail-segmentation",
    "13-covid-outbreak-prediction",
]
FORBIDDEN_DIRS = {"__pycache__", ".cache", ".pytest_cache", ".ruff_cache", ".mypy_cache", ".ipynb_checkpoints", ".venv", "venv", "env"}
PERSONAL_PATH = re.compile(r"(?:[A-Za-z]:[\\/](?:Users|Documents|Downloads)|/Users/|/home/[^/]+/|/workspace/)")
SECRET = re.compile(r"(?:AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:api[_-]?key|secret|token)\s*[=:]\s*['\"][^'\"]{12,})", re.I)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)")


def _local_link_failures(markdown: Path) -> list[str]:
    failures = []
    text = markdown.read_text(encoding="utf-8")
    for match in LINK.finditer(text):
        target = next(value for value in match.groups() if value)
        target = target.strip("<>").split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")): continue
        if not (markdown.parent / target).resolve().exists(): failures.append(f"broken link in {markdown.relative_to(ROOT)}: {target}")
    return failures


def _validate_project(project: Path) -> list[str]:
    failures = []
    required = ["README.md", "PROJECT_SUMMARY.md", "data/README.md", "src/analysis.py", "notebooks/01_end_to_end_analysis.ipynb", "reports/metrics.json"]
    for item in required:
        if not (project / item).is_file(): failures.append(f"missing {project.name}/{item}")
    if failures: return failures
    ast.parse((project / "src" / "analysis.py").read_text(encoding="utf-8"))
    metrics = json.loads((project / "reports" / "metrics.json").read_text(encoding="utf-8"))
    if metrics.get("status") != "passed": failures.append(f"{project.name}: metrics status is not passed")
    if not list((project / "reports" / "figures").glob("*.png")): failures.append(f"{project.name}: no figure")
    if not list((project / "reports" / "tables").glob("*.csv")): failures.append(f"{project.name}: no evidence table")
    notebook_path = project / "notebooks" / "01_end_to_end_analysis.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    code = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]
    if len(notebook.get("cells", [])) < 30: failures.append(f"{project.name}: fewer than 30 narrative notebook cells")
    if len(code) < 9: failures.append(f"{project.name}: fewer than 9 code cells")
    if any(cell.get("execution_count") is None for cell in code): failures.append(f"{project.name}: unexecuted code cell")
    if sum(bool(cell.get("outputs")) for cell in code) < 8: failures.append(f"{project.name}: insufficient saved outputs")
    if any(output.get("output_type") == "error" for cell in code for output in cell.get("outputs", [])): failures.append(f"{project.name}: saved notebook error")
    for cell in code: ast.parse("".join(cell.get("source", [])))
    for markdown in [project / "README.md", project / "PROJECT_SUMMARY.md", project / "data" / "README.md"]:
        failures.extend(_local_link_failures(markdown))
    return failures


def main() -> int:
    failures = []
    projects = sorted(path.name for path in (ROOT / "projects").iterdir() if path.is_dir())
    if projects != EXPECTED: failures.append(f"project set mismatch: {projects}")
    required_root = ["README.md", "PORTFOLIO_AUDIT.md", "PROJECT_STATUS_MATRIX.md", "MODEL_RESULTS_SUMMARY.md", "REPRODUCIBILITY_REPORT.md", "CHANGELOG.md", "GITHUB_PUSH_GUIDE.md", "DELIVERY_REPORT.md", "RUN_INSTRUCTIONS.md", "setup.ps1", "run_all.ps1", "setup_and_run.ps1", "run_all.py", "pyproject.toml"]
    for item in required_root:
        if not (ROOT / item).is_file(): failures.append(f"missing root file: {item}")
    for slug in EXPECTED:
        project_failures = _validate_project(ROOT / "projects" / slug)
        print(f"{'PASS' if not project_failures else 'FAIL'} {slug}")
        failures.extend(project_failures)
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        # Local virtual environments and generated caches are intentionally
        # ignored during source validation. They are already excluded from Git
        # and release archives and are expected to exist after a local run.
        if any(part in FORBIDDEN_DIRS for part in relative.parts):
            continue
        if path.is_dir() and path.name == ".git" and path.parent != ROOT: failures.append(f"nested Git directory: {path.relative_to(ROOT)}")
        if path.is_file() and path != Path(__file__).resolve() and path.suffix.lower() in {".py", ".md", ".ps1", ".toml", ".yml", ".yaml", ".json"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if PERSONAL_PATH.search(text): failures.append(f"machine-specific path: {path.relative_to(ROOT)}")
            if SECRET.search(text): failures.append(f"secret-like string: {path.relative_to(ROOT)}")
    for markdown in [ROOT / "README.md", ROOT / "RUN_INSTRUCTIONS.md", ROOT / "DELIVERY_REPORT.md"]:
        if markdown.is_file(): failures.extend(_local_link_failures(markdown))
    print("=" * 72)
    if failures:
        for failure in failures: print(f"FAIL {failure}")
        print(f"Summary: {len(EXPECTED)} projects checked, {len(failures)} failures")
        return 1
    print("Summary: 13 pass, 0 warnings, 0 failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
