# Run Instructions

This repository supports **Python 3.12 and 3.13** on Windows, macOS, and Linux. The notebooks already contain saved outputs, so GitHub can display the results without rerunning them.

## Windows PowerShell — recommended

Open PowerShell in the repository root and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup_and_run.ps1
```

The script selects Python 3.13 when available and otherwise Python 3.12, creates `.venv`, installs the locked dependency ranges, runs all 13 pipelines, regenerates and executes all notebooks, creates the reports, validates the repository, and runs the tests.

To separate installation and execution:

```powershell
.\setup.ps1
.\run_all.ps1
```

For a faster rerun that refreshes pipeline artifacts but keeps the existing notebook outputs:

```powershell
.\.venv\Scripts\python.exe run_all.py --quick
```

## Manual Windows commands

```powershell
py -3.13 -m venv .venv
# If 3.13 is unavailable, use: py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebooks]"
python run_all.py
```

## macOS or Linux

```bash
python3.13 -m venv .venv  # python3.12 is also supported
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev,notebooks]'
python run_all.py
```

## Run one project

```powershell
python projects\04-insurance-claim-prediction\src\analysis.py
python scripts\generate_portfolio_content.py
python scripts\execute_notebooks.py --project 04-insurance-claim-prediction
python scripts\generate_portfolio_reports.py
python validate_portfolio.py
```

## Verify without retraining

```powershell
python validate_portfolio.py
python -m unittest discover -s tests -v
```

The full run is CPU-based and may take several minutes. No API keys, GPU, cloud service, or external database is required. See [REPRODUCIBILITY_REPORT.md](REPRODUCIBILITY_REPORT.md) for the last recorded execution.
