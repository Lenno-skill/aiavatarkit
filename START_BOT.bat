@echo off
REM Start-Script für VRChat Meeting Moderator Bot
REM Aktiviert venv und startet den Bot

echo ========================================
echo VRChat Meeting Moderator Bot - Start
echo ========================================
echo.

REM Prüfe ob venv existiert
if not exist "venv_moderator" (
    echo FEHLER: Virtuelle Umgebung nicht gefunden!
    echo Führe zuerst setup_moderator_env.bat aus.
    pause
    exit /b 1
)

REM Aktiviere venv
echo Aktiviere virtuelle Umgebung...
call venv_moderator\Scripts\activate.bat

REM Prüfe Setup
echo.
echo Prüfe Setup...
python check_setup.py
echo.

REM Starte Bot
echo.
echo Starte Bot...
echo.
python vrchat_moderator.py

pause
