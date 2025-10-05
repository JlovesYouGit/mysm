@echo off
echo ========================================
echo Telecom API - Python FastAPI
echo ========================================
echo.

set PYTHON_PATH=python

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Install Python 3.9+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Install dependencies
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip uninstall -y motor pymongo 2>nul
pip install -r requirements.txt

echo.
echo Starting server on http://localhost:8081
echo API docs: http://localhost:8081/docs
echo.

python main.py
