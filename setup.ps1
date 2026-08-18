$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$PythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if (-not $PythonLauncher) { throw "Python launcher 'py' was not found. Install Python 3.12 or 3.13 from python.org." }

$Version = & py -3.12 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    $Version = & py -3.13 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
}
if ($LASTEXITCODE -ne 0) { throw "Python 3.12 or 3.13 is required." }

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating .venv with Python $Version..." -ForegroundColor Cyan
    & py "-$Version" -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[notebooks,dev]"
& .\.venv\Scripts\python.exe scripts\check_runtime.py
Write-Host "Environment setup completed." -ForegroundColor Green

