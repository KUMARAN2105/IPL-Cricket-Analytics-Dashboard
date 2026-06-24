# Open the first Power BI report found in the powerbi folder.
# Run this from the repository root in PowerShell.

$reportFolder = Join-Path (Get-Location) 'powerbi'
if (-not (Test-Path $reportFolder)) {
    Write-Error "The powerbi folder was not found."
    exit 1
}

$reportFile = Get-ChildItem -Path $reportFolder -Include *.pbix, *.pbit -File -Recurse | Select-Object -First 1
if (-not $reportFile) {
    Write-Host "No Power BI report file found in '$reportFolder'."
    Write-Host "Please add a .pbix or .pbit file to the powerbi folder and try again."
    exit 1
}

Write-Host "Opening Power BI report: $($reportFile.FullName)"
Start-Process -FilePath $reportFile.FullName
