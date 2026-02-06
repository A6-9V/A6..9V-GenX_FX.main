@echo off
REM Quick Status Check
cd /d "%~dp0"
powershell.exe -ExecutionPolicy Bypass -File "%~dp0check-status.ps1"
pause

