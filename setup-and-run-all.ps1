# Combined Setup Script for EXNESS Docker and Jules CLI
# This script sets up Docker services and installs Jules CLI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXNESS Docker + Jules CLI Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to refresh environment variables
function Refresh-Environment {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Part 1: Docker Setup
Write-Host "=== Part 1: Docker Setup ===" -ForegroundColor Yellow
Write-Host ""

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Write-Host ""
}

# Check Docker daemon
Write-Host "Checking Docker daemon..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
    $dockerRunning = $true
} catch {
    Write-Host "✗ Docker daemon is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and run this script again" -ForegroundColor Yellow
    $dockerRunning = $false
}

if ($dockerRunning) {
    # Navigate to script directory
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $scriptPath
    
    # Setup environment
    Write-Host "Setting up environment..." -ForegroundColor Yellow
    & "$scriptPath\setup-env.ps1"
    
    # Create directories
    Write-Host "Creating directories..." -ForegroundColor Yellow
    $directories = @("logs", "data", "init-db", "grafana/provisioning")
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "✓ Created: $dir" -ForegroundColor Green
        }
    }
    
    # Build and start
    Write-Host ""
    Write-Host "Building Docker images..." -ForegroundColor Yellow
    docker-compose build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker images built" -ForegroundColor Green
        
        Write-Host "Starting Docker containers..." -ForegroundColor Yellow
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Docker containers started" -ForegroundColor Green
            Start-Sleep -Seconds 5
            
            Write-Host ""
            Write-Host "Container Status:" -ForegroundColor Cyan
            docker-compose ps
        } else {
            Write-Host "✗ Failed to start containers" -ForegroundColor Red
        }
    } else {
        Write-Host "✗ Failed to build images" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "[SKIP] Docker setup skipped - Docker Desktop not running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Part 2: Jules CLI Installation ===" -ForegroundColor Yellow
Write-Host ""

# Refresh environment
Refresh-Environment

# Check Node.js
$nodeInstalled = $false
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "✓ Node.js installed: $nodeVersion" -ForegroundColor Green
        $nodeInstalled = $true
    }
} catch {
    # Not found
}

if (-not $nodeInstalled) {
    Write-Host "Node.js not found. Installing..." -ForegroundColor Yellow
    winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements --silent
    
    Start-Sleep -Seconds 5
    Refresh-Environment
    
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-Host "✓ Node.js installed: $nodeVersion" -ForegroundColor Green
            $nodeInstalled = $true
        }
    } catch {
        Write-Host "⚠ Node.js installation may require a new terminal session" -ForegroundColor Yellow
    }
}

if ($nodeInstalled) {
    try {
        $npmVersion = npm --version 2>$null
        Write-Host "✓ npm available: $npmVersion" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Installing Jules CLI..." -ForegroundColor Yellow
        npm install -g @google/jules
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Jules CLI installed" -ForegroundColor Green
            
            try {
                $julesVersion = jules --version 2>$null
                Write-Host "✓ Jules CLI version: $julesVersion" -ForegroundColor Green
            } catch {
                Write-Host "⚠ Run 'jules --version' in a new terminal to verify" -ForegroundColor Yellow
            }
        } else {
            Write-Host "✗ Failed to install Jules CLI" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ npm not available" -ForegroundColor Red
    }
} else {
    Write-Host "[SKIP] Jules CLI installation skipped - Node.js not available" -ForegroundColor Yellow
    Write-Host "Please restart your terminal and run this script again" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Docker Services:" -ForegroundColor Yellow
Write-Host "  - Trading Bridge API: http://localhost:8000" -ForegroundColor Green
Write-Host "  - Trading Bridge Port: localhost:5555" -ForegroundColor Green
Write-Host "  - Grafana: http://localhost:3000 (admin/admin)" -ForegroundColor Green
Write-Host ""
Write-Host "Jules CLI:" -ForegroundColor Yellow
Write-Host "  - Run 'jules login' to authenticate" -ForegroundColor Green
Write-Host "  - Run 'jules version' to verify" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. If Docker Desktop wasn't running, start it and run: docker-compose up -d" -ForegroundColor Cyan
Write-Host "  2. If Node.js was just installed, restart terminal and run: npm install -g @google/jules" -ForegroundColor Cyan
Write-Host "  3. Connect MT5 EA to bridge port 5555" -ForegroundColor Cyan
Write-Host ""

