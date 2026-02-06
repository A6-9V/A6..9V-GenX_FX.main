# Stop EXNESS Docker Services

Write-Host "Stopping EXNESS Docker containers..." -ForegroundColor Yellow

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Docker containers stopped successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to stop Docker containers" -ForegroundColor Red
    exit 1
}

