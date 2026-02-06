# Launch EXNESS Docker Services
# This script sets up and launches Docker containers for EXNESS terminal

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXNESS Docker Setup and Launch" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is running
Write-Host "Checking Docker daemon..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker daemon is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop" -ForegroundColor Yellow
    exit 1
}

# Navigate to project root directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent $scriptPath
Set-Location $rootPath

# Setup environment file
Write-Host "Setting up environment file..." -ForegroundColor Yellow
& "$scriptPath\setup-env.ps1"

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
$directories = @("logs", "data", "init-db", "grafana/provisioning")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created directory: $dir" -ForegroundColor Green
    }
}

# Build and start containers
Write-Host ""
Write-Host "Building Docker images..." -ForegroundColor Yellow
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to build Docker images" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Docker images built successfully" -ForegroundColor Green

Write-Host ""
Write-Host "Starting Docker containers..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start Docker containers" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Docker containers started successfully" -ForegroundColor Green

# Wait a moment for services to initialize
Start-Sleep -Seconds 5

# Show container status
Write-Host ""
Write-Host "Container Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Services Available:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Trading Bridge API: http://localhost:8000" -ForegroundColor Green
Write-Host "Trading Bridge Port: localhost:5555" -ForegroundColor Green
Write-Host "Grafana Dashboard: http://localhost:3000 (admin/admin)" -ForegroundColor Green
Write-Host "PostgreSQL: localhost:5432" -ForegroundColor Green
Write-Host "Redis: localhost:6379" -ForegroundColor Green
Write-Host "InfluxDB: http://localhost:8086" -ForegroundColor Green
Write-Host ""
Write-Host "To view logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "To stop: docker-compose down" -ForegroundColor Yellow
Write-Host ""

