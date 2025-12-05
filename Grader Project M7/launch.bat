@echo off
setlocal EnableDelayedExpansion
title M7Pro Grader - CTI-110 Assessment System
color 0A

echo.
echo  ========================================
echo    M7Pro Grader - Starting Application
echo  ========================================
echo.

:: Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Running setup...
    call create_venv.bat
)

:: Activate virtual environment
echo Activating virtual environment...
call "venv\Scripts\activate.bat"

:: Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not found! Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Flask application...
echo.
echo  Server will start at: http://127.0.0.1:5000
echo  Press Ctrl+C to stop the server
echo.
echo  ========================================
echo.

:: Start Flask app
python app.py

pause