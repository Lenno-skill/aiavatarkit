@echo off
REM Setup-Script für VRChat Meeting Moderator Bot
REM Erstellt eine virtuelle Umgebung und installiert alle Dependencies

echo ========================================
echo VRChat Meeting Moderator Bot - Setup
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH!
    echo Bitte installiere Python 3.10 oder höher von https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python-Version prüfen...
python --version
echo.

REM Erstelle virtuelle Umgebung
echo [2/5] Erstelle virtuelle Umgebung...
if exist "venv_moderator" (
    echo Virtuelle Umgebung existiert bereits. Überspringe...
) else (
    python -m venv venv_moderator
    if errorlevel 1 (
        echo FEHLER: Konnte virtuelle Umgebung nicht erstellen!
        pause
        exit /b 1
    )
    echo Virtuelle Umgebung erstellt.
)
echo.

REM Aktiviere virtuelle Umgebung
echo [3/5] Aktiviere virtuelle Umgebung...
call venv_moderator\Scripts\activate.bat
if errorlevel 1 (
    echo FEHLER: Konnte virtuelle Umgebung nicht aktivieren!
    pause
    exit /b 1
)
echo Virtuelle Umgebung aktiviert.
echo.

REM Upgrade pip
echo [4/5] Upgrade pip...
python -m pip install --upgrade pip
echo.

REM Installiere AIAvatarKit
echo [5/5] Installiere Dependencies...
echo.
echo Installiere AIAvatarKit (aus lokalem Verzeichnis)...
pip install -e .
if errorlevel 1 (
    echo FEHLER: Konnte AIAvatarKit nicht installieren!
    echo Versuche alternative Installation...
    pip install aiavatar
    if errorlevel 1 (
        echo FEHLER: Konnte AIAvatarKit nicht installieren!
        pause
        exit /b 1
    )
)
echo.

echo Installiere alle Moderator-Dependencies...
pip install -r requirements_all.txt
if errorlevel 1 (
    echo WARNUNG: Einige Dependencies konnten nicht installiert werden.
    echo Versuche alternative Installation...
    pip install -r requirements_moderator.txt
    if errorlevel 1 (
        echo FEHLER: Konnte Moderator-Dependencies nicht installieren!
        pause
        exit /b 1
    )
)
echo.

echo ========================================
echo Setup abgeschlossen!
echo ========================================
echo.
echo Um die virtuelle Umgebung zu aktivieren, führe aus:
echo   venv_moderator\Scripts\activate.bat
echo.
echo Dann kannst du den Bot starten mit:
echo   python vrchat_moderator.py
echo.
pause
