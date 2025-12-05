@echo off

echo Checking the Virtual Environment...
if exist ".\venv" (
    echo Virtual Environment already exists.
) else (
    echo Creating Virtual Environment using python...
    python -m venv venv
    echo Virtual Environment created successfully.
)

echo.
echo Activating the Virtual Environment...
call venv\Scripts\activate.bat || (
    echo ERROR: Could not activate venv. Check if Python venv exists.
    pause
    exit /b
)

echo.
echo Installing dependencies...
call dependencies.bat install_log.txt

echo.
echo Environment setup completed successfully!
pause