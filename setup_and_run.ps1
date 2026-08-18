$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
& "$Root\setup.ps1"
if ($LASTEXITCODE -ne 0) { throw "Setup failed." }
& "$Root\run_all.ps1"
if ($LASTEXITCODE -ne 0) { throw "Portfolio run failed." }

