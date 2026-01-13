#!/bin/bash
# Start-Script für VRChat Meeting Moderator Bot
# Aktiviert venv und startet den Bot

echo "========================================"
echo "VRChat Meeting Moderator Bot - Start"
echo "========================================"
echo ""

# Prüfe ob venv existiert
if [ ! -d "venv_moderator" ]; then
    echo "FEHLER: Virtuelle Umgebung nicht gefunden!"
    echo "Führe zuerst ./setup_moderator_env.sh aus."
    exit 1
fi

# Aktiviere venv
echo "Aktiviere virtuelle Umgebung..."
source venv_moderator/bin/activate

# Prüfe Setup
echo ""
echo "Prüfe Setup..."
python check_setup.py
echo ""

# Starte Bot
echo ""
echo "Starte Bot..."
echo ""
python vrchat_moderator.py
