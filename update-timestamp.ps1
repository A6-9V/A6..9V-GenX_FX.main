# Update Timestamp Script
# Updates date/time references in configuration files

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$date = Get-Date -Format "yyyy-MM-dd"
$time = Get-Date -Format "HH:mm:ss"

Write-Host "Updating timestamps..." -ForegroundColor Yellow
Write-Host "Current Date/Time: $timestamp" -ForegroundColor Cyan
Write-Host ""

# Update system-info.json
$systemInfoPath = "config/system-info.json"
if (Test-Path $systemInfoPath) {
    $systemInfo = Get-Content $systemInfoPath | ConvertFrom-Json
    $systemInfo.system_info.last_updated = $timestamp
    $systemInfo | ConvertTo-Json -Depth 10 | Set-Content $systemInfoPath
    Write-Host "✓ Updated $systemInfoPath" -ForegroundColor Green
}

# Update SETUP-STATUS.md
$setupStatusPath = "SETUP-STATUS.md"
if (Test-Path $setupStatusPath) {
    $content = Get-Content $setupStatusPath -Raw
    $content = $content -replace "Last Updated.*", "**Last Updated**: $timestamp"
    Set-Content $setupStatusPath -Value $content -NoNewline
    Write-Host "✓ Updated $setupStatusPath" -ForegroundColor Green
}

# Update DEMO-SETUP.md
$demoSetupPath = "DEMO-SETUP.md"
if (Test-Path $demoSetupPath) {
    $content = Get-Content $demoSetupPath -Raw
    $content = $content -replace "Last Updated.*", "**Last Updated**: $timestamp"
    Set-Content $demoSetupPath -Value $content -NoNewline
    Write-Host "✓ Updated $demoSetupPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Timestamp update complete!" -ForegroundColor Green
Write-Host "Current Date/Time: $timestamp" -ForegroundColor Cyan

