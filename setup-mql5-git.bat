@echo off
REM Setup MQL5 Git Repository
cd /d "%~dp0"
powershell.exe -ExecutionPolicy Bypass -File "%~dp0setup-mql5-git.ps1"
pause

