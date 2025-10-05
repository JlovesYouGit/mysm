@echo off
echo ========================================
echo Telecom Service - Windows Installer
echo ========================================
echo.

set PHP_PATH=N:\sms\php\php.exe
set COMPOSER_PATH=N:\sms\composer.bat

REM Check PHP
if not exist "%PHP_PATH%" (
    echo [ERROR] PHP not found at %PHP_PATH%
    pause
    exit /b 1
)

echo [OK] PHP found
"%PHP_PATH%" -v
echo.

REM Check Composer
if not exist "%COMPOSER_PATH%" (
    echo [ERROR] Composer not found at %COMPOSER_PATH%
    pause
    exit /b 1
)

echo [OK] Composer found
echo.

REM Check MongoDB
sc query MongoDB >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] MongoDB service not found
    echo Install from: https://www.mongodb.com/try/download/community
    echo.
)

echo Installing dependencies...
call "%COMPOSER_PATH%" install

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Composer install failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Quick Start:
echo 1. start_server.bat
echo 2. start_worker.bat (in new terminal)
echo 3. test_api.bat
echo.
echo See WINDOWS_SETUP.md for details
echo.
pause
