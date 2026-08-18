"""One-command portfolio rebuild, execution, test, and reporting runner."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(command: list[str], log) -> float:
    started = time.perf_counter(); printable = " ".join(command)
    print(f"\nRUN {printable}", flush=True); log.write(f"\nRUN {printable}\n"); log.flush()
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True); log.write(line); log.flush()
    code = process.wait()
    if code: raise RuntimeError(f"Command failed with exit code {code}: {printable}")
    return time.perf_counter() - started


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--quick", action="store_true", help="Run pipelines and validation but do not rebuild notebook outputs")
    args = parser.parse_args(); logs = ROOT / "execution_logs"; logs.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"); log_path = logs / f"run_all_{stamp}.log"
    timings = {}; started = time.perf_counter()
    try:
        with log_path.open("w", encoding="utf-8") as log:
            timings["runtime_check"] = run([sys.executable, "scripts/check_runtime.py"], log)
            for script in sorted((ROOT / "projects").glob("*/src/analysis.py")):
                timings[script.parents[1].name] = run([sys.executable, str(script.relative_to(ROOT))], log)
            timings["content_generation"] = run([sys.executable, "scripts/generate_portfolio_content.py"], log)
            if not args.quick: timings["notebook_execution"] = run([sys.executable, "scripts/execute_notebooks.py"], log)
            timings["portfolio_reports"] = run([sys.executable, "scripts/generate_portfolio_reports.py"], log)
            timings["validation"] = run([sys.executable, "validate_portfolio.py"], log)
            timings["tests"] = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], log)
        summary = {"status": "passed", "completed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "mode": "quick" if args.quick else "full", "total_seconds": round(time.perf_counter() - started, 3), "phase_seconds": {key: round(value, 3) for key, value in timings.items()}, "log": str(log_path.relative_to(ROOT))}
        (logs / "latest_run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"\nPORTFOLIO RUN PASSED in {summary['total_seconds']:.1f}s\nLog: {summary['log']}")
        return 0
    except Exception as error:
        failure = {"status": "failed", "completed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "error": str(error), "log": str(log_path.relative_to(ROOT))}
        (logs / "latest_run_summary.json").write_text(json.dumps(failure, indent=2), encoding="utf-8")
        print(f"\nPORTFOLIO RUN FAILED: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

