@echo off
echo ========================================
echo   M7Pro Grader - EXE Builder
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Installing/Updating PyInstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller!
    pause
    exit /b 1
)

echo.
echo Verifying PyInstaller installation...
python -m PyInstaller --version
if errorlevel 1 (
    echo ERROR: PyInstaller still not working!
    echo.
    echo Try this manually:
    echo   1. venv\Scripts\activate
    echo   2. pip uninstall pyinstaller
    echo   3. pip install pyinstaller
    echo   4. python -m PyInstaller --version
    pause
    exit /b 1
)

echo.
echo Building executable...
echo This may take 2-5 minutes...
echo.

REM Clean old builds
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

echo.
echo Starting PyInstaller (using python -m)...
echo.

REM Build the EXE using python -m PyInstaller
python -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --console ^
    --name M7Pro_Grader ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import flask ^
    --hidden-import flask.cli ^
    --hidden-import pandas ^
    --hidden-import matplotlib ^
    --hidden-import matplotlib.pyplot ^
    --hidden-import matplotlib.backends.backend_agg ^
    --hidden-import openpyxl ^
    --hidden-import openpyxl.styles ^
    --hidden-import openpyxl.drawing.image ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import requests ^
    --hidden-import numpy ^
    --collect-all flask ^
    --collect-all matplotlib ^
    app.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   BUILD FAILED!
    echo ========================================
    echo.
    echo Check the error messages above.
    echo.
    echo Common fixes:
    echo   1. pip cache purge
    echo   2. pip install --upgrade pip
    echo   3. pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD SUCCESSFUL!
echo ========================================
echo.

if exist "dist\M7Pro_Grader.exe" (
    echo Your executable is located at:
    echo   dist\M7Pro_Grader.exe
    echo.
    dir dist\M7Pro_Grader.exe | find "M7Pro_Grader.exe"
    echo.
    
    echo Creating backup copy...
    copy dist\M7Pro_Grader.exe .\M7Pro_Grader_FINAL.exe >nul
    echo Backup saved as: M7Pro_Grader_FINAL.exe
    echo.
    
    echo ========================================
    echo   NEXT STEPS:
    echo ========================================
    echo.
    echo 1. TEST THE EXE:
    echo    cd dist
    echo    M7Pro_Grader.exe
    echo.
    echo 2. CLEAN UP BUILD FILES (after testing):
    echo    cleanup_build.bat
    echo.
    echo ========================================
) else (
    echo ERROR: EXE file not found after build!
    echo Something went wrong during packaging.
)

echo.
pause