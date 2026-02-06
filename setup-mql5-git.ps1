# Setup MQL5 Git Repository
# Configures Git repository for MQL5 code

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MQL5 Git Repository Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$mql5Path = "C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06\MQL5"
$repoUrl = "https://forge.mql5.io/LengKundee/mql5.git"
$username = "LengKundee"
$password = "BLHwT8Pw"

# Check if MQL5 directory exists
if (-not (Test-Path $mql5Path)) {
    Write-Host "✗ MQL5 directory not found: $mql5Path" -ForegroundColor Red
    exit 1
}

Write-Host "MQL5 Path: $mql5Path" -ForegroundColor Yellow
Set-Location $mql5Path

# Check if already a git repository
if (Test-Path ".git") {
    Write-Host "✓ Git repository already exists" -ForegroundColor Green
    
    # Check remote
    $remote = git remote get-url origin 2>$null
    if ($remote) {
        Write-Host "  Current remote: $remote" -ForegroundColor White
    } else {
        Write-Host "  No remote configured" -ForegroundColor Yellow
        Write-Host "  Adding remote..." -ForegroundColor Yellow
        git remote add origin $repoUrl
    }
} else {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    
    Write-Host "Adding remote..." -ForegroundColor Yellow
    git remote add origin $repoUrl
}

# Configure Git credentials
Write-Host ""
Write-Host "Configuring Git credentials..." -ForegroundColor Yellow

# Store credentials in URL format
$credentialUrl = "https://${username}:${password}@forge.mql5.io/LengKundee/mql5.git"
git remote set-url origin $credentialUrl

Write-Host "✓ Remote configured" -ForegroundColor Green

# Configure Git user (if not already set)
$gitUser = git config user.name 2>$null
if (-not $gitUser) {
    Write-Host "Setting Git user..." -ForegroundColor Yellow
    git config user.name "LengKundee"
    git config user.email "lengkundee@example.com"
}

# Create .gitignore if not exists
if (-not (Test-Path ".gitignore")) {
    Write-Host "Creating .gitignore..." -ForegroundColor Yellow
    @"
# MQL5 Build artifacts
*.ex5
*.ex4
*.mq5.bak
*.mq4.bak

# Compiled files
*.log
*.txt

# Cache
*.cache

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✓ .gitignore created" -ForegroundColor Green
}

# Check repository status
Write-Host ""
Write-Host "Repository Status:" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: $repoUrl" -ForegroundColor White
Write-Host "Location: $mql5Path" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Add files: git add ." -ForegroundColor White
Write-Host "  2. Commit: git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "  3. Push: git push -u origin main" -ForegroundColor White
Write-Host ""

