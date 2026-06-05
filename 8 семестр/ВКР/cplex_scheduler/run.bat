@echo off
chcp 65001 > nul
set QT_QPA_PLATFORM_PLUGIN_PATH=venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python main.py
) else (
    echo Сначала запустите install_and_run.bat
    pause
)
