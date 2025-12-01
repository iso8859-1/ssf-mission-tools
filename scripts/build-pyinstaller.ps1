<#
Build script for PyInstaller one-file executable on Windows.

Usage (PowerShell):
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\scripts\build-pyinstaller.ps1

This script creates `dist\ssf-tools.exe`.
#>

$ErrorActionPreference = 'Stop'

Write-Host "Installing dev dependencies (pyinstaller)..."
python -m pip install -r requirements-dev.txt

Write-Host "Cleaning previous build/dist..."
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build,dist,__pycache__,ssf-tools.exe

# Use project spec if present, otherwise run direct
$spec = Join-Path $PSScriptRoot "..\build\ssf_tools.spec"
if (Test-Path $spec) {
    Write-Host "Using spec: $spec"
    pyinstaller --clean --noconfirm $spec
} else {
    Write-Host "No spec found; building from __main__.py"
    pyinstaller --onefile --name ssf-tools --console src\ssf_mission_tools\__main__.py
}

if (Test-Path dist\ssf-tools.exe) {
    Write-Host "Build succeeded: dist\ssf-tools.exe"
} else {
    Write-Error "Build failed or output not found. Check PyInstaller logs above."
}
