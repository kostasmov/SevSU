@echo off
chcp 65001 > nul
echo ================================================
echo  Установка и запуск программы оптимизации КС
echo ================================================
echo.

REM Проверка Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    echo Установите Python 3.10+ с сайта https://python.org
    echo При установке поставьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/4] Python найден:
python --version
echo.

REM Создание виртуального окружения (если нет)
if not exist "venv" (
    echo [2/4] Создание виртуального окружения...
    python -m venv venv
) else (
    echo [2/4] Виртуальное окружение уже существует.
)
echo.

REM Активация окружения
echo [3/4] Активация окружения и установка пакетов...
call venv\Scripts\activate.bat

REM Установка пакетов
pip install --quiet --upgrade pip
pip install PyQt5 matplotlib numpy openpyxl pulp

echo.
echo [4/4] Запуск программы...
echo.
python main.py

pause
