# Test Demo Account Connection
# This script helps verify the demo account setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXNESS Demo Account Connection Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check configuration files
Write-Host "Checking configuration files..." -ForegroundColor Yellow

$configFiles = @(
    "config/brokers.json",
    "config/symbols.json",
    "config/mt5-demo.json"
)

foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ Missing: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Demo Account Details:" -ForegroundColor Cyan
Write-Host "  Account: 279410452" -ForegroundColor White
Write-Host "  Server: Exness-MT5Trial8" -ForegroundColor White
Write-Host "  Type: Demo/Testing" -ForegroundColor White
Write-Host ""

# Check Docker services
Write-Host "Checking Docker services..." -ForegroundColor Yellow
try {
    $containers = docker-compose ps --format json 2>$null | ConvertFrom-Json
    $running = $containers | Where-Object { $_.State -eq "running" }
    
    if ($running.Count -gt 0) {
        Write-Host "✓ Docker services running: $($running.Count) containers" -ForegroundColor Green
        foreach ($container in $running) {
            Write-Host "  - $($container.Name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "⚠ Docker services not running" -ForegroundColor Yellow
        Write-Host "  Run: docker-compose up -d" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠ Cannot check Docker status" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Testing API endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing 2>$null
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Bridge API is accessible" -ForegroundColor Green
        $health = $response.Content | ConvertFrom-Json
        Write-Host "  Status: $($health.status)" -ForegroundColor Gray
        Write-Host "  MT5 Connected: $($health.mt5_connected)" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠ Bridge API not accessible (port 8000)" -ForegroundColor Yellow
    Write-Host "  Ensure Docker services are running" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Connect MT5 to Demo Account:" -ForegroundColor Yellow
Write-Host "   - Login: 279410452" -ForegroundColor White
Write-Host "   - Server: Exness-MT5Trial8" -ForegroundColor White
Write-Host "   - Password: Leng3A69V[@Una]" -ForegroundColor White
Write-Host ""
Write-Host "2. Attach EA to chart:" -ForegroundColor Yellow
Write-Host "   - BridgePort: 5555" -ForegroundColor White
Write-Host "   - BrokerName: EXNESS_DEMO" -ForegroundColor White
Write-Host ""
Write-Host "3. Verify symbols in Market Watch" -ForegroundColor Yellow
Write-Host "   - 20 symbols configured" -ForegroundColor White
Write-Host "   - See config/symbols.json for list" -ForegroundColor White
Write-Host ""
Write-Host "4. Check DEMO-SETUP.md for detailed instructions" -ForegroundColor Yellow
Write-Host ""

