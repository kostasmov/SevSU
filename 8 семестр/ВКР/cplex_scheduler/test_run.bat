@echo off
chcp 65001 > nul
echo ================================================
echo  Model test (without GUI, console only)
echo ================================================
echo.
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)
python tests/test_model.py
echo.
pause
