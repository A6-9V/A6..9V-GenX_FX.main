# Migration Script for New Directory Structure
# Helps users migrate from old structure to new organized structure

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXNESS Docker Structure Migration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent $scriptPath
Set-Location $rootPath

Write-Host "This script will help you migrate to the new directory structure." -ForegroundColor Yellow
Write-Host ""

# Check if migration is needed
$needsMigration = $false

if (Test-Path "Dockerfile" -PathType Leaf) {
    Write-Host "⚠ Found old Dockerfile in root - needs migration" -ForegroundColor Yellow
    $needsMigration = $true
}

if (Test-Path "requirements.txt" -PathType Leaf) {
    Write-Host "⚠ Found old requirements.txt in root - needs migration" -ForegroundColor Yellow
    $needsMigration = $true
}

if (-not $needsMigration) {
    Write-Host "✓ Directory structure appears to be already migrated" -ForegroundColor Green
    Write-Host ""
    Write-Host "Current structure looks good!" -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Migration Steps:" -ForegroundColor Cyan
Write-Host "1. Backup existing configuration" -ForegroundColor White
Write-Host "2. Create .env file from template" -ForegroundColor White
Write-Host "3. Verify all paths" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue with migration? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Migration cancelled." -ForegroundColor Yellow
    exit 0
}

# Backup
Write-Host ""
Write-Host "Creating backup..." -ForegroundColor Yellow
$backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

if (Test-Path ".env") {
    Copy-Item ".env" "$backupDir\.env.backup"
    Write-Host "✓ Backed up .env file" -ForegroundColor Green
}

if (Test-Path "docker-compose.yml") {
    Copy-Item "docker-compose.yml" "$backupDir\docker-compose.yml.backup"
    Write-Host "✓ Backed up docker-compose.yml" -ForegroundColor Green
}

Write-Host "Backup created in: $backupDir" -ForegroundColor Green

# Create .env from template
Write-Host ""
Write-Host "Setting up .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✓ Created .env from .env.example" -ForegroundColor Green
        Write-Host "  Please edit .env with your credentials!" -ForegroundColor Yellow
    } else {
        Write-Host "⚠ .env.example not found - please create .env manually" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Verify structure
Write-Host ""
Write-Host "Verifying directory structure..." -ForegroundColor Yellow

$requiredDirs = @("docker/trading-bridge", "config", "scripts", "docs", "bridge", "logs", "data")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Missing: $dir" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migration Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your credentials" -ForegroundColor White
Write-Host "2. Run: .\scripts\launch-docker.ps1" -ForegroundColor White
Write-Host "3. Verify services: docker-compose ps" -ForegroundColor White
Write-Host ""
Write-Host "Backup location: $backupDir" -ForegroundColor Gray
Write-Host ""

