# Install Jules CLI Script
# This script installs Node.js (if needed) and then installs Jules CLI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Jules CLI Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to refresh environment variables
function Refresh-Environment {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Check if Node.js is installed
$nodeInstalled = $false
Refresh-Environment
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "[OK] Node.js is already installed: $nodeVersion" -ForegroundColor Green
        $nodeInstalled = $true
    }
} catch {
    # Node.js not found
}

if (-not $nodeInstalled) {
    Write-Host "[INFO] Node.js not found. Installing Node.js LTS..." -ForegroundColor Yellow
    
    # Install Node.js via winget
    Write-Host "Installing Node.js via winget..." -ForegroundColor Yellow
    winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements --silent
    
    # Wait for installation
    Start-Sleep -Seconds 5
    
    # Refresh environment again
    Refresh-Environment
    
    # Check again
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-Host "[OK] Node.js installed: $nodeVersion" -ForegroundColor Green
            $nodeInstalled = $true
        }
    } catch {
        Write-Host "[WARNING] Node.js installation may require a new terminal session." -ForegroundColor Yellow
        Write-Host "Please restart your terminal and run this script again, or install Node.js manually from https://nodejs.org/" -ForegroundColor Yellow
    }
}

if (-not $nodeInstalled) {
    Write-Host "[ERROR] Cannot proceed without Node.js. Exiting." -ForegroundColor Red
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version 2>$null
    Write-Host "[OK] npm is available: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] npm not found. Please reinstall Node.js." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installing Jules CLI globally..." -ForegroundColor Cyan
npm install -g @google/jules

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Installation successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Verify installation
    try {
        $julesVersion = jules --version 2>$null
        if ($julesVersion) {
            Write-Host "Jules CLI version: $julesVersion" -ForegroundColor Green
        }
    } catch {
        Write-Host "[INFO] Run 'jules --version' in a new terminal to verify" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Run: jules login" -ForegroundColor Yellow
    Write-Host "2. Run: jules version (to verify)" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERROR] Failed to install Jules CLI" -ForegroundColor Red
    Write-Host "You may need to run this script as Administrator" -ForegroundColor Yellow
    exit 1
}

