#!/bin/bash
# Setup-Script für VRChat Meeting Moderator Bot
# Erstellt eine virtuelle Umgebung und installiert alle Dependencies

echo "========================================"
echo "VRChat Meeting Moderator Bot - Setup"
echo "========================================"
echo ""

# Prüfe ob Python installiert ist
if ! command -v python3 &> /dev/null; then
    echo "FEHLER: Python 3 ist nicht installiert!"
    echo "Bitte installiere Python 3.10 oder höher"
    exit 1
fi

echo "[1/5] Python-Version prüfen..."
python3 --version
echo ""

# Erstelle virtuelle Umgebung
echo "[2/5] Erstelle virtuelle Umgebung..."
if [ -d "venv_moderator" ]; then
    echo "Virtuelle Umgebung existiert bereits. Überspringe..."
else
    python3 -m venv venv_moderator
    if [ $? -ne 0 ]; then
        echo "FEHLER: Konnte virtuelle Umgebung nicht erstellen!"
        exit 1
    fi
    echo "Virtuelle Umgebung erstellt."
fi
echo ""

# Aktiviere virtuelle Umgebung
echo "[3/5] Aktiviere virtuelle Umgebung..."
source venv_moderator/bin/activate
if [ $? -ne 0 ]; then
    echo "FEHLER: Konnte virtuelle Umgebung nicht aktivieren!"
    exit 1
fi
echo "Virtuelle Umgebung aktiviert."
echo ""

# Upgrade pip
echo "[4/5] Upgrade pip..."
pip install --upgrade pip
echo ""

# Installiere AIAvatarKit
echo "[5/5] Installiere Dependencies..."
echo ""
echo "Installiere AIAvatarKit (aus lokalem Verzeichnis)..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "FEHLER: Konnte AIAvatarKit nicht installieren!"
    echo "Versuche alternative Installation..."
    pip install aiavatar
    if [ $? -ne 0 ]; then
        echo "FEHLER: Konnte AIAvatarKit nicht installieren!"
        exit 1
    fi
fi
echo ""

echo "Installiere alle Moderator-Dependencies..."
pip install -r requirements_all.txt
if [ $? -ne 0 ]; then
    echo "WARNUNG: Einige Dependencies konnten nicht installiert werden."
    echo "Versuche alternative Installation..."
    pip install -r requirements_moderator.txt
    if [ $? -ne 0 ]; then
        echo "FEHLER: Konnte Moderator-Dependencies nicht installieren!"
        exit 1
    fi
fi
echo ""

echo "========================================"
echo "Setup abgeschlossen!"
echo "========================================"
echo ""
echo "Um die virtuelle Umgebung zu aktivieren, führe aus:"
echo "  source venv_moderator/bin/activate"
echo ""
echo "Dann kannst du den Bot starten mit:"
echo "  python vrchat_moderator.py"
echo ""
