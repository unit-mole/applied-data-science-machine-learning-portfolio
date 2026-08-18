$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
if (-not (Test-Path ".venv\Scripts\python.exe")) { throw "The .venv environment is missing. Run .\setup.ps1 first." }
& .\.venv\Scripts\python.exe run_all.py
if ($LASTEXITCODE -ne 0) { throw "Portfolio execution failed. Review execution_logs\latest_run_summary.json." }
Write-Host "All 13 projects, notebooks, validation checks, and tests passed." -ForegroundColor Green

