@echo off
chcp 65001 > nul
set QT_PLUGIN_PATH=%~dp0venv\Lib\site-packages\PyQt5\Qt5\plugins

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python main.py
) else (
    echo Firstly run the install_and_run.bat
    pause
)
