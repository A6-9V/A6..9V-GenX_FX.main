@echo off
echo ========================================
echo EXNESS Docker Quickstart
echo ========================================
echo.

REM Check if Docker Desktop is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is NOT running!
    echo.
    echo Please:
    echo   1. Open Docker Desktop application
    echo   2. Wait for it to fully start
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Docker Desktop is running
echo.

REM Navigate to project root
cd /d "%~dp0\.."

echo Starting Docker services...
docker-compose up -d

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start services
    echo Trying to build first...
    docker-compose build
    docker-compose up -d
)

echo.
echo ========================================
echo Services Status
echo ========================================
docker-compose ps

echo.
echo ========================================
echo Quickstart Complete!
echo ========================================
echo.
echo IMPORTANT: Configure your account in .env file
echo   - Copy env.template to .env (or run scripts\setup-env.ps1)
echo   - Edit .env with your EXNESS credentials
echo   - See docs\CONFIGURATION.md for details
echo.
echo Services:
echo   - Bridge API: http://localhost:8000
echo   - Bridge Port: localhost:5555
echo   - Grafana: http://localhost:3000
echo.
echo Next: Connect MT5 to demo account and attach EA
echo.
pause

