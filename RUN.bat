@echo off
echo ========================================
echo Telecom API - Quick Start
echo ========================================
echo.

echo [1] Starting services...
powershell -ExecutionPolicy Bypass -File "start-telecom.ps1"

echo.
echo [2] Waiting 5 seconds for startup...
timeout /t 5 /nobreak >nul

echo.
echo [3] Running API tests...
call test_api_py.bat

echo.
echo ========================================
echo Services Running:
echo - API: http://localhost:8081/docs
echo - Panel: http://localhost:8081/static/index.html
echo - WebSocket: ws://localhost:8081/ws/events
echo ========================================
pause