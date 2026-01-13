# Quick Start - VRChat Meeting Moderator Bot

Schnellstart-Anleitung für den VRChat Meeting Moderator Bot.

## Voraussetzungen Checkliste

Bevor du startest, stelle sicher dass du hast:

- [ ] **Python 3.10+** installiert
- [ ] **OpenAI API Key** (von https://platform.openai.com/api-keys)
- [ ] **VB-CABLE** installiert (beide Geräte: A und B)
- [ ] **VRChat** installiert (Desktop-Modus)
- [ ] **VOICEVOX** (optional, aber empfohlen)

## Schritt 1: Setup-Script ausführen

### Windows:
```cmd
setup_moderator_env.bat
```

### Linux/Mac:
```bash
chmod +x setup_moderator_env.sh
./setup_moderator_env.sh
```

Das Script erstellt automatisch:
- ✅ Virtuelle Umgebung (`venv_moderator`)
- ✅ Installiert alle Dependencies
- ✅ Konfiguriert alles für dich

## Schritt 2: Audio-Geräte konfigurieren

### 2.1 VB-CABLE Indizes finden:

```cmd
# Aktiviere venv zuerst!
venv_moderator\Scripts\activate.bat

python
>>> from aiavatar.device import AudioDevice
>>> AudioDevice().list_audio_devices()
```

Notiere dir:
- **VRChat_INPUT_DEVICE**: Index von "CABLE-B Output" (Bot hört VRChat)
- **VRChat_OUTPUT_DEVICE**: Index von "CABLE-A Input" (Bot spricht zu VRChat)

### 2.2 Windows Sound-Einstellungen:

1. **VB-Cable-B Input** als Standard-Ausgabegerät setzen:
   - Windows Einstellungen → System → Sound
   - Standard-Ausgabegerät: "CABLE-B Input (VB-Audio Virtual Cable)"

## Schritt 3: Umgebungsvariablen setzen

Erstelle eine `.env` Datei im Projektverzeichnis:

```bash
# .env
OPENAI_API_KEY=sk-dein-api-key-hier
VRChat_INPUT_DEVICE=6      # Dein Index von CABLE-B Output
VRChat_OUTPUT_DEVICE=13    # Dein Index von CABLE-A Input
VOICEVOX_URL=http://127.0.0.1:50021
VOICEVOX_SPEAKER=46
VISION_INTERVAL=3.0
OSC_HOST=127.0.0.1
OSC_PORT=9000
```

**Oder setze sie in der Kommandozeile:**

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-dein-api-key
set VRChat_INPUT_DEVICE=6
set VRChat_OUTPUT_DEVICE=13
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-dein-api-key"
$env:VRChat_INPUT_DEVICE="6"
$env:VRChat_OUTPUT_DEVICE="13"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-dein-api-key"
export VRChat_INPUT_DEVICE=6
export VRChat_OUTPUT_DEVICE=13
```

## Schritt 4: VRChat vorbereiten

1. **VRChat starten** (Desktop-Modus)
2. **Mit Bot-Account einloggen**
3. **Audio-Einstellungen**:
   - Mikrofon: **VB-Cable-A**
   - Lautsprecher: Standard (wird automatisch auf VB-Cable-B Input umgeleitet)
4. **OSC aktivieren**:
   - Settings → OSC → Enable OSC
   - Port: **9000**

## Schritt 5: VOICEVOX starten (optional)

Falls du VOICEVOX verwendest:

1. Starte VOICEVOX
2. Standard-Port: `http://127.0.0.1:50021`
3. Teste: `curl http://127.0.0.1:50021/speakers`

## Schritt 6: Bot starten

```cmd
# Aktiviere venv
venv_moderator\Scripts\activate.bat

# Starte Bot
python vrchat_moderator.py
```

**Erwartete Ausgabe:**
```
INFO - VRChat Meeting Moderator Bot gestartet
INFO - Warte auf Meeting-Teilnehmer...
INFO - Kontinuierliche Vision-Überwachung gestartet
```

## Schritt 7: In VRChat testen

1. Gehe in eine Welt mit anderen Teilnehmern
2. Sprich in VRChat
3. Bot sollte:
   - ✅ Audio empfangen
   - ✅ Antworten generieren
   - ✅ Sprechen (über VB-Cable-A)
   - ✅ Screenshots machen (alle 3 Sekunden)
   - ✅ Gesichtsausdrücke ändern (wenn FaceOSC konfiguriert)

## Häufige Probleme

### "ModuleNotFoundError: No module named 'aiavatar'"
**Lösung:** Stelle sicher, dass venv aktiviert ist und `pip install -e .` ausgeführt wurde

### "VB-Cable nicht gefunden"
**Lösung:** 
- Prüfe ob beide VB-Cable-Geräte installiert sind
- Starte Windows neu
- Prüfe Windows Sound-Einstellungen

### "OpenAI API Fehler"
**Lösung:**
- Prüfe ob API Key korrekt gesetzt ist: `echo %OPENAI_API_KEY%` (Windows) oder `echo $OPENAI_API_KEY` (Linux/Mac)
- Prüfe API-Quota auf https://platform.openai.com/usage

### "Vision funktioniert nicht"
**Lösung:**
- Stelle sicher, dass VRChat-Fenster sichtbar ist
- Prüfe ob `pyautogui` installiert ist: `pip list | grep pyautogui`
- Bei Multi-Monitor: Setze `VRChat_WINDOW_REGION` Umgebungsvariable

## Nächste Schritte

Nach erfolgreichem Start:

1. **Avatar konfigurieren**: Siehe SETUP_ANLEITUNG.md für FaceOSC Setup
2. **System Prompt anpassen**: Bearbeite `create_moderation_system_prompt()` in `vrchat_moderator.py`
3. **Fine-Tuning**: Passe Vision-Intervalle und andere Parameter an

## Vollständige Dokumentation

Für detaillierte Informationen siehe:
- **SETUP_ANLEITUNG.md** - Vollständige Setup-Anleitung
- **README_MODERATOR.md** - Bot-Dokumentation
- **README.md** - AIAvatarKit Hauptdokumentation

## Support

Bei Problemen:
1. Prüfe die Logs (Debug-Modus ist standardmäßig aktiviert)
2. Siehe SETUP_ANLEITUNG.md für Troubleshooting
3. Prüfe ob alle Voraussetzungen erfüllt sind

Viel Erfolg! 🚀
