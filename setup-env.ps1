# Setup Environment File
# Creates .env file from template if it doesn't exist

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent $scriptPath
$envFile = Join-Path $rootPath ".env"
$envExample = Join-Path $rootPath ".env.example"
$envTemplate = Join-Path $rootPath "env.template"

# Determine which template to use
$templateFile = $null
if (Test-Path $envExample) {
    $templateFile = $envExample
    Write-Host "Found .env.example template" -ForegroundColor Green
} elseif (Test-Path $envTemplate) {
    $templateFile = $envTemplate
    Write-Host "Found env.template (using as fallback)" -ForegroundColor Yellow
} else {
    Write-Host "Warning: No environment template found!" -ForegroundColor Red
    Write-Host "  Expected: .env.example or env.template in root directory" -ForegroundColor Yellow
    Write-Host "  Please create .env file manually" -ForegroundColor Yellow
    exit 1
}

# Create .env from template if it doesn't exist
if (-not (Test-Path $envFile)) {
    if ($templateFile) {
        Copy-Item $templateFile $envFile
        Write-Host "✓ Created .env file from template" -ForegroundColor Green
        Write-Host "⚠ IMPORTANT: Edit .env file with your EXNESS credentials!" -ForegroundColor Yellow
        Write-Host "  Required: EXNESS_LOGIN, EXNESS_PASSWORD, EXNESS_SERVER" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
    Write-Host "  (Skipping template copy)" -ForegroundColor Gray
}

