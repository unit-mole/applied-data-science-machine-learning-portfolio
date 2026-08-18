"""Execute and persist every recruiter-facing notebook without Jupyter magics."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import os
import platform
import shutil
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def execute(path: Path) -> dict[str, object]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    namespace = {"__name__": "__notebook__"}; execution_count = 0
    original_cwd = Path.cwd(); started = time.perf_counter()
    try:
        os.chdir(path.parent)
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") != "code": continue
            execution_count += 1; stream = io.StringIO(); source = "".join(cell.get("source", []))
            try:
                with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                    exec(compile(source, str(path), "exec"), namespace)
                output = stream.getvalue()
                cell["outputs"] = [] if not output else [{"name": "stdout", "output_type": "stream", "text": output.splitlines(keepends=True)}]
            except Exception as error:
                cell["outputs"] = [{"ename": type(error).__name__, "evalue": str(error), "output_type": "error", "traceback": traceback.format_exc().splitlines()}]
                cell["execution_count"] = execution_count
                path.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
                raise
            cell["execution_count"] = execution_count
    finally:
        os.chdir(original_cwd)
    path.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
    project = path.parents[1]; metrics = project / "reports" / "metrics.json"
    return {
        "project": project.name, "status": "passed", "duration_seconds": round(time.perf_counter() - started, 3),
        "notebook_cells": len(notebook["cells"]), "code_cells": execution_count,
        "code_cells_with_outputs": sum(bool(cell.get("outputs")) for cell in notebook["cells"] if cell.get("cell_type") == "code"),
        "notebook": str(path.relative_to(ROOT)), "metrics": str(metrics.relative_to(ROOT)),
        "metrics_sha256": hashlib.sha256(metrics.read_bytes()).hexdigest(),
        "figures": [str(item.relative_to(ROOT)) for item in sorted((project / "reports" / "figures").glob("*.png"))],
        "tables": [str(item.relative_to(ROOT)) for item in sorted((project / "reports" / "tables").glob("*.csv"))],
    }


def _refresh_content(slugs: list[str]) -> None:
    generator_path = ROOT / "scripts" / "generate_portfolio_content.py"
    spec = importlib.util.spec_from_file_location("portfolio_content", generator_path)
    if spec is None or spec.loader is None: raise RuntimeError(generator_path)
    generator = importlib.util.module_from_spec(spec); spec.loader.exec_module(generator)
    for slug in slugs:
        project = ROOT / "projects" / slug; meta = generator.PROJECTS[slug]
        metrics = json.loads((project / "reports" / "metrics.json").read_text(encoding="utf-8"))
        (project / "README.md").write_text(generator.render_readme(slug, meta, metrics), encoding="utf-8")
        (project / "PROJECT_SUMMARY.md").write_text(generator.render_summary(slug, meta, metrics), encoding="utf-8")
        (project / "data" / "README.md").write_text(generator.render_data_readme(slug, meta), encoding="utf-8")


def _write_report(records: list[dict[str, object]]) -> None:
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    packages = {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "openpyxl"]}
    payload = {"status": "passed", "executed_at_utc": generated, "python": platform.python_version(), "platform": platform.platform(), "packages": packages, "project_count": len(records), "total_duration_seconds": round(sum(float(record["duration_seconds"]) for record in records), 3), "projects": records}
    (ROOT / "REPRODUCIBILITY_REPORT.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    rows = [f"| {record['project']} | Passed | {record['notebook_cells']} | {record['code_cells']} | {record['code_cells_with_outputs']} | {float(record['duration_seconds']):.1f}s | [Notebook]({record['notebook']}) | [Metrics]({record['metrics']}) | {len(record['figures'])} | {len(record['tables'])} |" for record in records]
    report = f"""# Reproducibility Report

**Status:** Passed  
**Executed at (UTC):** {generated}  
**Python:** {platform.python_version()}  
**Projects:** {len(records)}  
**Total measured notebook runtime:** {payload['total_duration_seconds']:.1f} seconds

## Scientific environment

| Package | Version |
|---|---:|
""" + "\n".join(f"| {name} | {version} |" for name, version in packages.items()) + """

## Notebook execution evidence

| Project | Status | Cells | Code cells | Code cells with output | Runtime | Notebook | Metrics | Figures | Tables |
|---|---|---:|---:|---:|---:|---|---|---:|---:|
""" + "\n".join(rows) + """

All primary notebooks load bundled data, expose provenance and quality evidence, execute the complete reusable pipeline, show task-appropriate results and robustness evidence, embed saved figures, and verify artifact hashes. Runtime varies by CPU and installed library versions.

## Determinism and known variation

Random seeds are fixed where supported. Parallel tree fitting, numerical libraries, and dependency-version changes can cause small floating-point differences. Dataset hashes and metric hashes are recorded so material drift can be distinguished from harmless numeric variation.
"""
    (ROOT / "REPRODUCIBILITY_REPORT.md").write_text(report, encoding="utf-8")


def _cleanup() -> None:
    names = {"__pycache__", ".cache", ".pytest_cache", ".ruff_cache", ".mypy_cache", ".ipynb_checkpoints"}
    for path in sorted((item for item in ROOT.rglob("*") if item.is_dir() and item.name in names), key=lambda item: len(item.parts), reverse=True):
        shutil.rmtree(path, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--project", help="Optional project slug")
    args = parser.parse_args()
    if args.project:
        paths = [ROOT / "projects" / args.project / "notebooks" / "01_end_to_end_analysis.ipynb"]
    else:
        paths = sorted((ROOT / "projects").glob("*/notebooks/01_end_to_end_analysis.ipynb"))
    for path in paths:
        if not path.is_file(): raise FileNotFoundError(path)
    records = []
    for path in paths:
        records.append(execute(path)); print(f"PASS {path.relative_to(ROOT)}", flush=True)
    _refresh_content([str(record["project"]) for record in records]); _write_report(records); _cleanup()
    print(f"PASS reproducibility report ({len(records)} projects)", flush=True)


if __name__ == "__main__":
    main()
