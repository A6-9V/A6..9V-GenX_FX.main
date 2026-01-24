@echo off
echo GenX-FX Quick Start
call npm install
call npm run build
start "GenX-FX Backend" /min python -m uvicorn api.main:app --port 8081 --reload
start "GenX-FX Frontend" /min npx serve client/dist -p 3000
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8081