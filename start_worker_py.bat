@echo off
echo Starting Queue Worker...
echo.

call venv\Scripts\activate.bat
python worker.py
