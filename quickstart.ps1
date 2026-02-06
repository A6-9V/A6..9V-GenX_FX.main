# EXNESS Docker Quickstart Script
# Sets up and runs all services for demo account testing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXNESS Docker Quickstart" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Step 1: Check Docker
Write-Host "[1/5] Checking Docker Desktop..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
    $dockerRunning = $true
} catch {
    Write-Host "✗ Docker Desktop is NOT running" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "  1. Open Docker Desktop application" -ForegroundColor White
    Write-Host "  2. Wait for it to fully start (whale icon in system tray)" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Step 2: Setup Environment
Write-Host ""
Write-Host "[2/5] Setting up environment..." -ForegroundColor Yellow
& "$scriptPath\setup-env.ps1" | Out-Null

# Create directories
$directories = @("logs", "data", "init-db", "grafana/provisioning")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✓ Environment ready" -ForegroundColor Green

# Step 3: Build Images
Write-Host ""
Write-Host "[3/5] Building Docker images..." -ForegroundColor Yellow
docker-compose build --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Images built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to build images" -ForegroundColor Red
    exit 1
}

# Step 4: Start Services
Write-Host ""
Write-Host "[4/5] Starting Docker services..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Services started" -ForegroundColor Green
    
    # Wait for services to initialize
    Write-Host "  Waiting for services to initialize..." -ForegroundColor Gray
    Start-Sleep -Seconds 8
} else {
    Write-Host "✗ Failed to start services" -ForegroundColor Red
    exit 1
}

# Step 5: Verify Services
Write-Host ""
Write-Host "[5/5] Verifying services..." -ForegroundColor Yellow

# Check containers
$containers = docker-compose ps --format json 2>$null | ConvertFrom-Json
$running = $containers | Where-Object { $_.State -eq "running" }

if ($running.Count -gt 0) {
    Write-Host "✓ $($running.Count) containers running" -ForegroundColor Green
} else {
    Write-Host "⚠ No containers running" -ForegroundColor Yellow
}

# Test API
Start-Sleep -Seconds 2
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Bridge API is accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Bridge API not ready yet (may need a few more seconds)" -ForegroundColor Yellow
}

# Display Status
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Services Status" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Quickstart Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Demo Account Ready:" -ForegroundColor Cyan
Write-Host "  Account: 279410452" -ForegroundColor White
Write-Host "  Server: Exness-MT5Trial8" -ForegroundColor White
Write-Host "  Password: Leng3A69V[@Una]" -ForegroundColor White
Write-Host ""
Write-Host "Services Available:" -ForegroundColor Cyan
Write-Host "  • Trading Bridge API: http://localhost:8000" -ForegroundColor Green
Write-Host "  • Trading Bridge Port: localhost:5555" -ForegroundColor Green
Write-Host "  • Grafana Dashboard: http://localhost:3000 (admin/admin)" -ForegroundColor Green
Write-Host "  • PostgreSQL: localhost:5432" -ForegroundColor Green
Write-Host "  • Redis: localhost:6379" -ForegroundColor Green
Write-Host "  • InfluxDB: http://localhost:8086" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Connect MT5 to demo account (279410452)" -ForegroundColor White
Write-Host "  2. Attach EA to chart with BridgePort: 5555" -ForegroundColor White
Write-Host "  3. Select from 20 configured symbols" -ForegroundColor White
Write-Host ""
Write-Host "View logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "Stop services: docker-compose down" -ForegroundColor Gray
Write-Host ""

