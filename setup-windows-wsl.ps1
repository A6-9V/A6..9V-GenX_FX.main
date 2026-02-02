# GenX FX - Windows WSL Setup Script
# Run this script in PowerShell as Administrator to set up WSL for H: drive

Write-Host "========================================"  -ForegroundColor Cyan
Write-Host "GenX FX - Windows WSL Setup Script"  -ForegroundColor Cyan
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ Running with Administrator privileges" -ForegroundColor Green
Write-Host ""

# Function to print colored output
function Write-Success {
    param($message)
    Write-Host "✓ $message" -ForegroundColor Green
}

function Write-Warning {
    param($message)
    Write-Host "⚠ $message" -ForegroundColor Yellow
}

function Write-Error-Message {
    param($message)
    Write-Host "✗ $message" -ForegroundColor Red
}

# Step 1: Enable WSL Feature
Write-Host "Step 1: Checking WSL features..." -ForegroundColor Cyan
$wslFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

if ($wslFeature.State -eq "Enabled") {
    Write-Success "WSL feature is already enabled"
} else {
    Write-Warning "Enabling WSL feature..."
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    Write-Success "WSL feature enabled"
}

# Step 2: Enable Virtual Machine Platform
Write-Host ""
Write-Host "Step 2: Checking Virtual Machine Platform..." -ForegroundColor Cyan
$vmFeature = Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform

if ($vmFeature.State -eq "Enabled") {
    Write-Success "Virtual Machine Platform is already enabled"
} else {
    Write-Warning "Enabling Virtual Machine Platform..."
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    Write-Success "Virtual Machine Platform enabled"
}

# Step 3: Check WSL version and update
Write-Host ""
Write-Host "Step 3: Checking WSL version..." -ForegroundColor Cyan

try {
    $wslVersion = wsl --version 2>&1
    Write-Success "WSL is installed"
    Write-Host $wslVersion
} catch {
    Write-Warning "WSL not installed or needs update"
    Write-Host "Installing/Updating WSL..." -ForegroundColor Yellow
    wsl --install --no-distribution
    wsl --update
    Write-Success "WSL installed/updated"
}

# Step 4: Set WSL 2 as default
Write-Host ""
Write-Host "Step 4: Setting WSL 2 as default..." -ForegroundColor Cyan
wsl --set-default-version 2
Write-Success "WSL 2 set as default version"

# Step 5: Install Ubuntu (if not already installed)
Write-Host ""
Write-Host "Step 5: Checking Ubuntu installation..." -ForegroundColor Cyan

$ubuntuInstalled = wsl --list --quiet | Select-String -Pattern "Ubuntu"

if ($ubuntuInstalled) {
    Write-Success "Ubuntu is already installed"
} else {
    Write-Warning "Installing Ubuntu 22.04..."
    wsl --install -d Ubuntu-22.04
    Write-Success "Ubuntu 22.04 installed"
    Write-Warning "Please complete the Ubuntu setup (username and password) when prompted"
}

# Step 6: Copy .wslconfig to user profile
Write-Host ""
Write-Host "Step 6: Configuring WSL settings..." -ForegroundColor Cyan

$wslconfigSource = Join-Path $PSScriptRoot ".wslconfig"
$wslconfigDest = Join-Path $env:USERPROFILE ".wslconfig"

if (Test-Path $wslconfigSource) {
    Copy-Item $wslconfigSource $wslconfigDest -Force
    Write-Success ".wslconfig copied to $wslconfigDest"
} else {
    Write-Warning ".wslconfig not found in current directory"
    Write-Host "Creating default .wslconfig..." -ForegroundColor Yellow
    
    $wslConfigContent = @"
[wsl2]
memory=8GB
processors=6
swap=4GB
nestedVirtualization=true
pageReporting=true

[experimental]
sparseVhd=true
dnsTunneling=true
autoMemoryReclaim=gradual
networkingMode=mirrored
autoProxy=true
"@
    
    Set-Content -Path $wslconfigDest -Value $wslConfigContent
    Write-Success "Default .wslconfig created at $wslconfigDest"
}

# Step 7: Check Docker Desktop installation
Write-Host ""
Write-Host "Step 7: Checking Docker Desktop..." -ForegroundColor Cyan

$dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"

if (Test-Path $dockerPath) {
    Write-Success "Docker Desktop is installed"
    Write-Warning "Please ensure Docker Desktop has WSL 2 backend enabled in Settings"
} else {
    Write-Error-Message "Docker Desktop not found"
    Write-Host "Please download and install Docker Desktop from:" -ForegroundColor Yellow
    Write-Host "https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
}

# Step 8: Verify H: drive accessibility
Write-Host ""
Write-Host "Step 8: Checking H: drive..." -ForegroundColor Cyan

if (Test-Path "H:\") {
    Write-Success "H: drive is accessible"
    
    # Create Projects directory if it doesn't exist
    $projectsPath = "H:\Projects"
    if (-not (Test-Path $projectsPath)) {
        New-Item -ItemType Directory -Path $projectsPath -Force | Out-Null
        Write-Success "Created H:\Projects directory"
    } else {
        Write-Success "H:\Projects directory exists"
    }
    
} else {
    Write-Error-Message "H: drive not found"
    Write-Warning "Please ensure H: drive is properly mapped and accessible"
}

# Step 9: Restart WSL
Write-Host ""
Write-Host "Step 9: Restarting WSL..." -ForegroundColor Cyan
wsl --shutdown
Start-Sleep -Seconds 2
Write-Success "WSL restarted"

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open Ubuntu from Start Menu or run: wsl" -ForegroundColor White
Write-Host "2. Navigate to H: drive: cd /mnt/h/Projects" -ForegroundColor White
Write-Host "3. Clone the repository:" -ForegroundColor White
Write-Host "   git clone https://github.com/A6-9V/A6..9V-GenX_FX.main.git GenX_FX" -ForegroundColor Cyan
Write-Host "4. Enter the directory: cd GenX_FX" -ForegroundColor White
Write-Host "5. Run the setup script: ./setup-wsl.sh" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see: docs/WSL_H_DRIVE_SETUP.md" -ForegroundColor Yellow
Write-Host ""

# Check if restart is needed
if ($wslFeature.State -ne "Enabled" -or $vmFeature.State -ne "Enabled") {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "RESTART REQUIRED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Some Windows features require a restart to take effect." -ForegroundColor Yellow
    Write-Host "Please restart your computer before continuing." -ForegroundColor Yellow
    Write-Host ""
    
    $restart = Read-Host "Would you like to restart now? (Y/N)"
    if ($restart -eq "Y" -or $restart -eq "y") {
        Write-Host "Restarting in 10 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        Restart-Computer
    }
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
