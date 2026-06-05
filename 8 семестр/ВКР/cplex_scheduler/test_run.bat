@echo off
chcp 65001 > nul
echo ================================================
echo  Тест модели (без GUI, только консоль)
echo ================================================
echo.
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)
python tests/test_model.py
echo.
pause
