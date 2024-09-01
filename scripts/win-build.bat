@echo off

REM Pfade
SET ICON_PATH=..\MineMetrics.ico
SET SCRIPT_PATH=..\app\main.py
SET DIST_PATH=..\dist
SET BUILD_PATH=..\build
SET SPEC_PATH=..\spec

REM Entferne vorherige Builds
IF EXIST "%DIST_PATH%" rd /s /q "%DIST_PATH%"
IF EXIST "%BUILD_PATH%" rd /s /q "%BUILD_PATH%"
IF EXIST "%SPEC_PATH%" rd /s /q "%SPEC_PATH%"

REM PyInstaller-Befehl zum Erstellen eines Windows 64-Bit-Builds
pyinstaller --onefile --windowed --icon="%ICON_PATH%" --distpath "%DIST_PATH%" --workpath "%BUILD_PATH%" --specpath "%SPEC_PATH%" "%SCRIPT_PATH%"

echo Build completed successfully.
pause
