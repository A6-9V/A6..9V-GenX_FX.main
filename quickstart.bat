@echo off
REM EXNESS Docker Quickstart - Batch Launcher
cd /d "%~dp0"
powershell.exe -ExecutionPolicy Bypass -File "%~dp0quickstart.ps1"
if errorlevel 1 pause

