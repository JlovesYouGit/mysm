@echo off
echo Testing Telecom API...
echo.

REM Test login
echo [1/4] Testing login...
set PHP_PATH=N:\sms\php\php.exe

if not exist "%PHP_PATH%" (
    echo [ERROR] PHP not found
    pause
    exit /b 1
)

powershell -Command "$response = Invoke-WebRequest -Uri http://localhost:8080/api/auth/login -Method POST -Body '{\"username\":\"admin\",\"password\":\"telecom2025\"}' -ContentType 'application/json'; $json = $response.Content | ConvertFrom-Json; $json.token" > token.tmp

if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Login failed. Is server running?
    del token.tmp 2>nul
    pause
    exit /b 1
)

set /p TOKEN=<token.tmp
echo [OK] Token: %TOKEN%
echo.

REM Test SMS send
echo [2/4] Testing SMS send...
powershell -Command "Invoke-WebRequest -Uri http://localhost:8080/api/sms/send -Method POST -Headers @{Authorization='Bearer %TOKEN%'} -Body '{\"to\":\"+1234567890\",\"from\":\"+0987654321\",\"message\":\"Test\"}' -ContentType 'application/json'"
if %ERRORLEVEL% EQU 0 (echo [OK] SMS sent) else (echo [FAIL] SMS send failed)
echo.

REM Test SMS receive
echo [3/4] Testing SMS receive...
powershell -Command "Invoke-WebRequest -Uri http://localhost:8080/api/sms/receive -Method GET -Headers @{Authorization='Bearer %TOKEN%'}"
if %ERRORLEVEL% EQU 0 (echo [OK] SMS received) else (echo [FAIL] SMS receive failed)
echo.

REM Test numbers list
echo [4/4] Testing numbers list...
powershell -Command "Invoke-WebRequest -Uri http://localhost:8080/api/numbers -Method GET -Headers @{Authorization='Bearer %TOKEN%'}"
if %ERRORLEVEL% EQU 0 (echo [OK] Numbers listed) else (echo [FAIL] Numbers list failed)
echo.

del token.tmp 2>nul
echo.
echo Tests complete!
pause
