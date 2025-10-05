@echo off
echo Testing Python Telecom API...
echo.

REM Get token
echo [1/5] Login...
curl -X POST http://localhost:8081/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"telecom2025\"}" > response.json
for /f "tokens=2 delims=:," %%a in ('type response.json ^| findstr "token"') do set TOKEN=%%a
set TOKEN=%TOKEN:"=%
set TOKEN=%TOKEN: =%
echo Token: %TOKEN%
echo.

REM Send SMS
echo [2/5] Send SMS...
curl -X POST http://localhost:8081/api/sms/send -H "Authorization: Bearer %TOKEN%" -H "Content-Type: application/json" -d "{\"to\":\"+1234567890\",\"from_\":\"+0987654321\",\"message\":\"Test\"}"
echo.
echo.

REM Receive SMS
echo [3/5] Receive SMS...
curl -X GET http://localhost:8081/api/sms/receive -H "Authorization: Bearer %TOKEN%"
echo.
echo.

REM Make call
echo [4/5] Make call...
curl -X POST http://localhost:8081/api/voice/call -H "Authorization: Bearer %TOKEN%" -H "Content-Type: application/json" -d "{\"to\":\"+1234567890\",\"from_\":\"+0987654321\"}"
echo.
echo.

REM List numbers
echo [5/5] List numbers...
curl -X GET http://localhost:8081/api/numbers -H "Authorization: Bearer %TOKEN%"
echo.
echo.

del response.json 2>nul
echo Tests complete!
pause
