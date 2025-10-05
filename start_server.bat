@echo off
echo Starting Telecom Service...
echo.

REM Check if PHP is available
where php >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PHP not found. Run install.bat first.
    pause
    exit /b 1
)

REM Start MongoDB if not running
sc query MongoDB | find "RUNNING" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Starting MongoDB...
    net start MongoDB
)

echo.
echo Server starting on http://localhost:8080
echo Press Ctrl+C to stop
echo.

php -S localhost:8080 -t N:\sms
