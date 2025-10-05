@echo off
echo Starting Queue Worker...
echo Press Ctrl+C to stop
echo.

set PHP_PATH=N:\sms\php\php.exe

if not exist "%PHP_PATH%" (
    echo [ERROR] PHP not found at %PHP_PATH%
    pause
    exit /b 1
)

"%PHP_PATH%" N:\sms\queue_worker.php
