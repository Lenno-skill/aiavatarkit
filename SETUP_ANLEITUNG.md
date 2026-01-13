# VRChat Meeting Moderator Bot - Vollständige Setup-Anleitung

Diese Anleitung führt dich Schritt für Schritt durch die komplette Einrichtung des VRChat Meeting Moderator Bots.

## Übersicht der benötigten Komponenten

1. ✅ **Python 3.10+** - Programmiersprache
2. ✅ **Virtuelle Umgebung (venv)** - Isolierte Python-Umgebung
3. ✅ **AIAvatarKit** - Haupt-Framework
4. ✅ **Moderator Dependencies** - Zusätzliche Pakete
5. ⚠️ **VOICEVOX** - Text-to-Speech (optional, aber empfohlen)
6. ⚠️ **VB-CABLE** - Virtuelle Audio-Geräte (ERFORDERLICH)
7. ⚠️ **VRChat** - Desktop-Anwendung (ERFORDERLICH)
8. ⚠️ **OpenAI API Key** - Für LLM und STT (ERFORDERLICH)

## Schritt 1: Python Installation

### Windows:
1. Lade Python 3.10 oder höher von https://www.python.org/downloads/
2. Während der Installation: **WICHTIG**: Aktiviere "Add Python to PATH"
3. Installiere Python

### Linux/Mac:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Mac (mit Homebrew)
brew install python@3.10
```

### Verifikation:
```bash
python --version
# Sollte zeigen: Python 3.10.x oder höher
```

## Schritt 2: Virtuelle Umgebung erstellen

### Windows:
```cmd
# Führe das Setup-Script aus:
setup_moderator_env.bat

# ODER manuell:
python -m venv venv_moderator
venv_moderator\Scripts\activate.bat
```

### Linux/Mac:
```bash
# Mache das Script ausführbar:
chmod +x setup_moderator_env.sh

# Führe das Setup-Script aus:
./setup_moderator_env.sh

# ODER manuell:
python3 -m venv venv_moderator
source venv_moderator/bin/activate
```

### Verifikation:
Nach der Aktivierung sollte dein Prompt so aussehen:
```
(venv_moderator) C:\...>
```

## Schritt 3: Dependencies installieren

Die Dependencies werden automatisch vom Setup-Script installiert. Falls du es manuell machen möchtest:

```bash
# Stelle sicher, dass die venv aktiviert ist
# Dann:
pip install --upgrade pip
pip install -e .  # Installiert AIAvatarKit aus dem lokalen Verzeichnis
pip install -r requirements_moderator.txt
```

### Verifikation:
```bash
pip list | grep aiavatar
# Sollte aiavatar zeigen
```

## Schritt 4: VOICEVOX Installation (Optional, aber empfohlen)

VOICEVOX ist ein japanisches Text-to-Speech-System. Es gibt mehrere Optionen:

### Option A: VOICEVOX Engine (Lokal)
1. Lade VOICEVOX von https://voicevox.hiroshiba.jp/
2. Installiere und starte VOICEVOX
3. Standard-Port: `http://127.0.0.1:50021`

### Option B: AivisSpeech (Alternative)
- Siehe https://aivis-project.com/ für Details

### Option C: Andere TTS-Services
- Du kannst auch Azure, Google, OpenAI TTS verwenden
- Siehe README.md für Konfiguration

### Verifikation:
```bash
# Teste ob VOICEVOX läuft:
curl http://127.0.0.1:50021/speakers
# Sollte eine JSON-Liste mit Sprechern zurückgeben
```

## Schritt 5: VB-CABLE Installation (ERFORDERLICH)

VB-CABLE ist **ERFORDERLICH** für die VRChat-Integration. Du brauchst **2 virtuelle Audio-Geräte**.

### Installation:
1. Lade VB-CABLE von https://vb-audio.com/Cable/
2. Installiere **VB-Cable-A** (kostenlos)
3. Installiere **VB-Cable-B** (kostenlos, separate Installation)
4. Starte Windows neu (empfohlen)

### Konfiguration:
1. **VB-Cable-B Input** als Standard-Ausgabegerät setzen:
   - Windows: Einstellungen → System → Sound → Standard-Ausgabegerät
   - Wähle "CABLE-B Input (VB-Audio Virtual Cable)"

2. **Audio-Geräte-Indizes finden**:
   ```python
   python
   >>> from aiavatar.device import AudioDevice
   >>> AudioDevice().list_audio_devices()
   ```
   
   Notiere dir:
   - Index von **"CABLE-B Output"** (Input-Device für Bot)
   - Index von **"CABLE-A Input"** (Output-Device für Bot)

### Verifikation:
- Prüfe Windows Sound-Einstellungen: Beide VB-Cable-Geräte sollten sichtbar sein
- Teste Audio: Spiele Musik ab, sollte über VB-Cable-B Input hörbar sein

## Schritt 6: OpenAI API Key besorgen

1. Gehe zu https://platform.openai.com/
2. Erstelle einen Account oder logge dich ein
3. Gehe zu API Keys: https://platform.openai.com/api-keys
4. Erstelle einen neuen API Key
5. **WICHTIG**: Kopiere den Key sofort (wird nur einmal angezeigt!)

### API Key setzen:

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-dein-api-key-hier
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-dein-api-key-hier"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-dein-api-key-hier"
```

**Oder erstelle eine `.env` Datei:**
```bash
# .env Datei im Projektverzeichnis
OPENAI_API_KEY=sk-dein-api-key-hier
```

### Verifikation:
```python
python
>>> import os
>>> print(os.getenv("OPENAI_API_KEY"))
# Sollte deinen API Key zeigen
```

## Schritt 7: VRChat Setup

### Installation:
1. Lade VRChat von https://hello.vrchat.com/
2. Installiere VRChat (Desktop-Modus)
3. Erstelle einen Account für den Bot

### Avatar-Konfiguration:

#### 1. FaceOSC Parameter hinzufügen:
1. Öffne dein Avatar in Unity
2. Im Animator: Füge Parameter `FaceOSC` hinzu
   - Typ: **Int**
   - Default: **0**
   - Saved: **false**
   - Synced: **true**
3. Im FX Animator Controller:
   - Füge `FaceOSC` Parameter hinzu
   - Erstelle States für verschiedene Gesichtsausdrücke:
     - 0: neutral
     - 1: attentive
     - 2: friendly
     - 3: thinking
     - 4: speaking
     - 5: listening
   - Erstelle Transitions basierend auf FaceOSC-Werten

#### 2. VRCEmote Parameter (optional für Animationen):
- Ähnlich wie FaceOSC, aber für Animationen
- Werte: 0=idling, 1=attention, 2=quiet, 3=pointing, 4=welcoming

#### 3. OSC aktivieren:
1. In VRChat: Settings → OSC
2. Aktiviere "Enable OSC"
3. Port sollte **9000** sein (Standard)

### Verifikation:
- VRChat sollte im Desktop-Modus laufen
- OSC sollte aktiviert sein
- Avatar sollte FaceOSC Parameter haben

## Schritt 8: Konfiguration des Bots

### Umgebungsvariablen setzen:

Erstelle eine `.env` Datei oder setze Umgebungsvariablen:

```bash
# .env Datei
OPENAI_API_KEY=sk-dein-api-key
VOICEVOX_URL=http://127.0.0.1:50021
VOICEVOX_SPEAKER=46
VRChat_INPUT_DEVICE=6      # Index von VB-Cable-B Output
VRChat_OUTPUT_DEVICE=13    # Index von VB-Cable-A Input
VISION_INTERVAL=3.0         # Sekunden zwischen Screenshots
OSC_HOST=127.0.0.1
OSC_PORT=9000
```

### Audio-Geräte-Indizes finden:

```python
# Aktiviere venv zuerst!
python
>>> from aiavatar.device import AudioDevice
>>> devices = AudioDevice().list_audio_devices()
>>> for d in devices:
...     if "CABLE" in d["name"].upper():
...         print(f"Index {d['index']}: {d['name']}")
```

## Schritt 9: Bot starten

### Vorbereitung:
1. ✅ Virtuelle Umgebung aktiviert
2. ✅ VOICEVOX läuft (falls verwendet)
3. ✅ VRChat gestartet (Desktop-Modus)
4. ✅ Bot-Account in VRChat eingeloggt
5. ✅ VB-Cable-A als Mikrofon in VRChat gesetzt
6. ✅ VB-Cable-B Input als Standard-Ausgabegerät in Windows

### Bot starten:

```bash
# Stelle sicher, dass venv aktiviert ist
python vrchat_moderator.py
```

### Erwartete Ausgabe:
```
INFO - VRChat Meeting Moderator Bot gestartet
INFO - Warte auf Meeting-Teilnehmer...
INFO - Kontinuierliche Vision-Überwachung gestartet
```

## Schritt 10: Testing

### Test 1: Audio-Verbindung
1. Sprich in VRChat
2. Bot sollte Audio empfangen (siehe Logs)
3. Bot sollte antworten können

### Test 2: Vision-System
1. Bot sollte automatisch Screenshots machen
2. Prüfe Logs für "Vision-Update" Meldungen
3. Bot sollte visuelle Updates erhalten

### Test 3: Face Expressions
1. Bot sollte Gesichtsausdrücke ändern
2. Prüfe VRChat Avatar: FaceOSC sollte sich ändern

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'aiavatar'"
**Lösung:**
- Stelle sicher, dass venv aktiviert ist
- Führe aus: `pip install -e .`

### Problem: "PyAudio nicht gefunden"
**Lösung:**
- Windows: Installiere Visual C++ Build Tools
- Oder: `pip install pipwin && pipwin install pyaudio`

### Problem: "VB-Cable nicht gefunden"
**Lösung:**
- Stelle sicher, dass beide VB-Cable-Geräte installiert sind
- Starte Windows neu
- Prüfe Windows Sound-Einstellungen

### Problem: "OSC-Verbindung fehlgeschlagen"
**Lösung:**
- Prüfe ob OSC in VRChat aktiviert ist
- Prüfe Port (sollte 9000 sein)
- Prüfe Firewall-Einstellungen

### Problem: "Vision funktioniert nicht"
**Lösung:**
- Stelle sicher, dass VRChat-Fenster sichtbar ist
- Prüfe ob `pyautogui` installiert ist
- Bei Multi-Monitor: Setze `VRChat_WINDOW_REGION`

### Problem: "OpenAI API Fehler"
**Lösung:**
- Prüfe ob API Key korrekt gesetzt ist
- Prüfe ob API Key gültig ist
- Prüfe API-Quota/Limits

## Nächste Schritte

Nach erfolgreichem Setup:

1. **Fine-Tuning**: Passe System Prompt an deine Bedürfnisse an
2. **Avatar-Optimierung**: Erweitere Face Expressions und Animationen
3. **Performance**: Für Produktion: Nutze PostgreSQL statt SQLite
4. **Erweiterte Features**: Integriere zusätzliche Tools oder Services

## Support

Bei Problemen:
1. Prüfe die Logs (Debug-Modus aktiviert)
2. Siehe README_MODERATOR.md für Details
3. Prüfe AIAvatarKit Dokumentation

## Checkliste

- [ ] Python 3.10+ installiert
- [ ] Virtuelle Umgebung erstellt und aktiviert
- [ ] Alle Dependencies installiert
- [ ] VOICEVOX installiert und läuft (optional)
- [ ] VB-CABLE installiert (beide Geräte)
- [ ] Audio-Geräte konfiguriert
- [ ] OpenAI API Key besorgt und gesetzt
- [ ] VRChat installiert und konfiguriert
- [ ] Avatar mit FaceOSC Parameter erstellt
- [ ] OSC in VRChat aktiviert
- [ ] Bot erfolgreich gestartet
- [ ] Audio-Verbindung funktioniert
- [ ] Vision-System funktioniert
- [ ] Face Expressions funktionieren

Viel Erfolg! 🚀
