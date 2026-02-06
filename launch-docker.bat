@echo off
REM Launch EXNESS Docker Services - Batch Script
cd /d "%~dp0\.."
powershell.exe -ExecutionPolicy Bypass -File "%~dp0launch-docker.ps1"
pause

