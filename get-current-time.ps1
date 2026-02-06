# Get Current Date and Time
# Quick script to display current system date/time

$dateTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$date = Get-Date -Format "yyyy-MM-dd"
$time = Get-Date -Format "HH:mm:ss"
$dayOfWeek = Get-Date -Format "dddd"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Current System Date/Time" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Date/Time: $dateTime" -ForegroundColor Green
Write-Host "Date:      $date" -ForegroundColor White
Write-Host "Time:      $time" -ForegroundColor White
Write-Host "Day:       $dayOfWeek" -ForegroundColor White
Write-Host ""
Write-Host "Timezone:  $(Get-TimeZone).Id" -ForegroundColor Gray
Write-Host ""

