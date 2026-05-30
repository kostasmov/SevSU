@echo off
chcp 65001 > nul
echo ================================================
echo  Installation and launch of the optimization program
echo ================================================
echo.

REM Check Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Install Python 3.10+ from https://python.org
    echo During installation check "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

REM Create virtual environment (if not exists)
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/4] Virtual environment already exists.
)
echo.

REM Activate environment
echo [3/4] Activating environment and installing packages...
call venv\Scripts\activate.bat

REM Install packages
pip install --quiet --upgrade pip
pip install PyQt5 matplotlib numpy openpyxl pulp

echo.
echo [4/4] Launching program...
echo.
python main.py

pause

