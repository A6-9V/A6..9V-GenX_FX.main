# EXNESS Docker Status Check
# Comprehensive check of all services and configuration

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXNESS Docker Status Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent $scriptPath
Set-Location $rootPath

$allGood = $true

# 1. Check Docker Desktop
Write-Host "[1/6] Checking Docker Desktop..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
    $dockerRunning = $true
} catch {
    Write-Host "✗ Docker Desktop is NOT running" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop first!" -ForegroundColor Yellow
    $dockerRunning = $false
    $allGood = $false
}

# 2. Check Docker Compose
Write-Host ""
Write-Host "[2/6] Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>$null
    if ($composeVersion) {
        Write-Host "✓ Docker Compose available" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Docker Compose not found (trying 'docker compose')" -ForegroundColor Yellow
}

# 3. Check Container Status
Write-Host ""
Write-Host "[3/6] Checking Container Status..." -ForegroundColor Yellow
if ($dockerRunning) {
    try {
        $containers = docker-compose ps --format json 2>$null | ConvertFrom-Json
        if ($containers) {
            $running = $containers | Where-Object { $_.State -eq "running" }
            $total = $containers.Count
            
            Write-Host "  Total containers: $total" -ForegroundColor White
            Write-Host "  Running: $($running.Count)" -ForegroundColor $(if ($running.Count -eq $total) { "Green" } else { "Yellow" })
            
            if ($running.Count -eq 0) {
                Write-Host "  ⚠ No containers running" -ForegroundColor Yellow
                $allGood = $false
            } elseif ($running.Count -lt $total) {
                Write-Host "  ⚠ Some containers not running" -ForegroundColor Yellow
                $allGood = $false
            }
            
            Write-Host ""
            foreach ($container in $containers) {
                $statusColor = if ($container.State -eq "running") { "Green" } else { "Red" }
                Write-Host "  $($container.Name): $($container.State)" -ForegroundColor $statusColor
            }
        } else {
            Write-Host "  ⚠ No containers found" -ForegroundColor Yellow
            $allGood = $false
        }
    } catch {
        Write-Host "  ✗ Cannot check container status" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "  [SKIP] Docker Desktop not running" -ForegroundColor Gray
}

# 4. Check Configuration Files
Write-Host ""
Write-Host "[4/6] Checking Configuration Files..." -ForegroundColor Yellow
$configFiles = @(
    "docker-compose.yml",
    "Dockerfile",
    "config/brokers.json",
    "config/symbols.json",
    "config/mt5-demo.json"
)

$missingFiles = @()
foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Missing: $file" -ForegroundColor Red
        $missingFiles += $file
        $allGood = $false
    }
}

# 5. Check Ports
Write-Host ""
Write-Host "[5/6] Checking Ports..." -ForegroundColor Yellow
$ports = @(
    @{Port=5555; Service="Bridge"},
    @{Port=8000; Service="API"},
    @{Port=3000; Service="Grafana"},
    @{Port=5432; Service="PostgreSQL"},
    @{Port=6379; Service="Redis"},
    @{Port=8086; Service="InfluxDB"}
)

foreach ($portInfo in $ports) {
    try {
        $result = Test-NetConnection -ComputerName localhost -Port $portInfo.Port -WarningAction SilentlyContinue -InformationLevel Quiet
        if ($result) {
            Write-Host "  ✓ Port $($portInfo.Port) ($($portInfo.Service)): Open" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Port $($portInfo.Port) ($($portInfo.Service)): Closed" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host "  ? Port $($portInfo.Port) ($($portInfo.Service)): Cannot check" -ForegroundColor Yellow
    }
}

# 6. Test API Health
Write-Host ""
Write-Host "[6/6] Testing API Health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✓ Bridge API is accessible" -ForegroundColor Green
        try {
            $health = $response.Content | ConvertFrom-Json
            Write-Host "    Status: $($health.status)" -ForegroundColor White
            Write-Host "    MT5 Connected: $($health.mt5_connected)" -ForegroundColor White
        } catch {
            Write-Host "    Response: $($response.Content)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "  ✗ Bridge API not accessible (http://localhost:8000)" -ForegroundColor Red
    Write-Host "    Services may not be running" -ForegroundColor Yellow
    $allGood = $false
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Status Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($allGood) {
    Write-Host "✓ All systems operational!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Services Available:" -ForegroundColor Cyan
    Write-Host "  • Trading Bridge API: http://localhost:8000" -ForegroundColor Green
    Write-Host "  • Trading Bridge Port: localhost:5555" -ForegroundColor Green
    Write-Host "  • Grafana Dashboard: http://localhost:3000" -ForegroundColor Green
} else {
    Write-Host "⚠ Issues detected - see details above" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Cyan
    if (-not $dockerRunning) {
        Write-Host "  1. Start Docker Desktop" -ForegroundColor White
    }
    if ($running.Count -eq 0 -and $dockerRunning) {
        Write-Host "  2. Start services: docker-compose up -d" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Demo Account:" -ForegroundColor Cyan
Write-Host "  Account: 279410452" -ForegroundColor White
Write-Host "  Server: Exness-MT5Trial8" -ForegroundColor White
Write-Host "  Symbols: 20 configured" -ForegroundColor White
Write-Host ""

