@echo off
echo ========================================
echo  Building Ark Config Switcher EXE
echo ========================================
echo.

echo Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    echo.
)

echo Building executable...
python -m PyInstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --name "Ark Config Switcher" ark_config_switcher.py

echo.
echo ========================================
echo  Build Complete!
echo ========================================
echo.
echo Your .exe file is located at:
echo   dist\ArkConfigSwitcher.exe
echo.
echo You can distribute this single file to users.
echo.
pause

