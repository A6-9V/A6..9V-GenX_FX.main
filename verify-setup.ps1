# Verify EXNESS Docker Setup
# Checks if all files and configurations are correct

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXNESS Docker Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Check required files
Write-Host "Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "launch-docker.ps1",
    "bridge/main.py",
    "config/brokers.json"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ Missing: $file" -ForegroundColor Red
        $errors++
    }
}

# Check directories
Write-Host ""
Write-Host "Checking directories..." -ForegroundColor Yellow
$requiredDirs = @(
    "bridge",
    "config",
    "logs",
    "data"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "✓ $dir/" -ForegroundColor Green
    } else {
        Write-Host "⚠ Missing: $dir/ (will be created on launch)" -ForegroundColor Yellow
        $warnings++
    }
}

# Check Docker
Write-Host ""
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✓ Docker installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found" -ForegroundColor Red
    $errors++
}

try {
    docker ps | Out-Null
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker daemon is not running" -ForegroundColor Red
    $errors++
}

# Check docker-compose
Write-Host ""
Write-Host "Checking docker-compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>&1
    Write-Host "✓ Docker Compose: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ Docker Compose not found (using 'docker compose' instead)" -ForegroundColor Yellow
    $warnings++
}

# Check environment file
Write-Host ""
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "⚠ .env file not found (will be created from template)" -ForegroundColor Yellow
    $warnings++
}

# Check MT5 path
Write-Host ""
Write-Host "Checking MT5 terminal path..." -ForegroundColor Yellow
$mt5Path = "C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06"
if (Test-Path $mt5Path) {
    Write-Host "✓ MT5 terminal path exists: $mt5Path" -ForegroundColor Green
} else {
    Write-Host "⚠ MT5 terminal path not found: $mt5Path" -ForegroundColor Yellow
    Write-Host "  (This is OK if MT5 is installed elsewhere)" -ForegroundColor Gray
    $warnings++
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($errors -eq 0) {
    Write-Host "✓ Setup verification complete!" -ForegroundColor Green
    if ($warnings -gt 0) {
        Write-Host "⚠ $warnings warning(s) found (non-critical)" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Ready to launch! Run: .\launch-docker.ps1" -ForegroundColor Green
} else {
    Write-Host "✗ Setup verification failed!" -ForegroundColor Red
    Write-Host "  $errors error(s) found" -ForegroundColor Red
    if ($warnings -gt 0) {
        Write-Host "  $warnings warning(s) found" -ForegroundColor Yellow
    }
}
Write-Host "========================================" -ForegroundColor Cyan

exit $errors

