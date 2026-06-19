@echo off
chcp 65001 > nul
echo ================================================
echo  Ustanovka i zapusk programmy optimizacii KS
echo ================================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python ne najden!
    echo Ustanovite Python 3.10+ s sajta https://python.org
    echo Pri ustanovke postavte galochku "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/4] Python najden:
python --version
echo.

echo [2/4] Ustanovka osnovnyh paketov (PyQt5, matplotlib, numpy, openpyxl)...
python -m pip install --quiet --upgrade pip
python -m pip install PyQt5 matplotlib numpy openpyxl

echo [3/4] Ustanovka reshatelej...
echo   - PuLP/CBC (besplatnyj, reshaet zadachi lyuboj razmernosti) - OBYAZATELNO
python -m pip install pulp
echo   - IBM CPLEX Community (docplex) - opcionalno, dlya malyh zadach
python -m pip install docplex cplex
if errorlevel 1 (
    echo   CPLEX ne ustanovilsya - ne strashno, budet ispolzovan PuLP/CBC.
)

echo.
echo [4/4] Zapusk programmy...
echo.
python main.py

pause
