# VRChat Meeting Moderator Bot

Ein AI-Moderator-Bot für VRChat-Meetings mit kontinuierlicher visueller Beobachtung und Echtzeit-Verhaltensanalyse der Teilnehmer.

## Features

- **Kontinuierliche Vision-Überwachung**: Automatische Screenshots alle 2-5 Sekunden
- **Echtzeit-Verhaltensanalyse**: Analyse von Teilnehmer-Verhalten, Engagement und Aktivitäten
- **Speaker Diarization**: Erkennung mehrerer Sprecher in Meetings
- **Moderation Tools**: Meeting-Notizen, Timer, Topic-Tracking, Zusammenfassungen
- **VRChat-Integration**: Face Expressions und Animationen über OSC

## Voraussetzungen

1. **Python 3.10+**
2. **VOICEVOX API** (läuft auf `http://127.0.0.1:50021`)
3. **OpenAI API Key** (für LLM und STT)
4. **VB-CABLE** (2 virtuelle Audio-Geräte für VRChat)
5. **VRChat** (Desktop-Modus)

## Installation

1. Installiere AIAvatarKit:
```bash
pip install aiavatar
```

2. Installiere zusätzliche Dependencies:
```bash
pip install -r requirements_moderator.txt
```

3. Installiere VB-CABLE:
   - Lade VB-CABLE von https://vb-audio.com/Cable/
   - Installiere VB-Cable-A und VB-Cable-B

## Konfiguration

### 1. Audio-Geräte konfigurieren

Führe Python aus und liste verfügbare Audio-Geräte auf:

```python
from aiavatar.device import AudioDevice
AudioDevice().list_audio_devices()
```

Notiere dir die Indizes für:
- **VB-Cable-B Output** (Input-Device für Bot - hört VRChat-Audio)
- **VB-Cable-A Input** (Output-Device für Bot - spricht zu VRChat)

### 2. Umgebungsvariablen setzen

Erstelle eine `.env` Datei oder setze Umgebungsvariablen:

```bash
export OPENAI_API_KEY="dein-openai-api-key"
export VRChat_INPUT_DEVICE=6   # Index von VB-Cable-B Output
export VRChat_OUTPUT_DEVICE=13 # Index von VB-Cable-A Input
export VOICEVOX_URL="http://127.0.0.1:50021"
export VOICEVOX_SPEAKER=46
export VISION_INTERVAL=3.0     # Sekunden zwischen Screenshots
export OSC_HOST="127.0.0.1"
export OSC_PORT=9000
```

### 3. VRChat Avatar konfigurieren

1. **FaceOSC Parameter hinzufügen**:
   - Öffne dein Avatar in Unity
   - Füge Parameter `FaceOSC` hinzu (Typ: int, Default: 0, Saved: false, Synced: true)
   - Füge Parameter zum FX Animator Controller hinzu
   - Erstelle States und Transitions für verschiedene Gesichtsausdrücke

2. **VRCEmote Parameter** (optional für Animationen):
   - Ähnlich wie FaceOSC, aber für Animationen

3. **OSC aktivieren**:
   - In VRChat: Settings → OSC → Enable OSC
   - Port sollte 9000 sein (oder entsprechend OSC_PORT anpassen)

## Verwendung

1. **VOICEVOX starten** (falls verwendet)

2. **VRChat starten** (Desktop-Modus)
   - Logge dich mit dem Bot-Account ein
   - Setze VB-Cable-A als Mikrofon in VRChat-Einstellungen
   - Setze VB-Cable-B Input als Standard-Ausgabegerät in Windows

3. **Moderator-Bot starten**:
```bash
python vrchat_moderator.py
```

4. **In VRChat**:
   - Gehe in eine Welt mit anderen Teilnehmern
   - Der Bot beginnt automatisch mit der Moderation
   - Der Bot beobachtet kontinuierlich das Meeting visuell

## Funktionsweise

### Kontinuierliche Vision-Überwachung

Der Bot macht automatisch Screenshots vom VRChat-Fenster:
- **Intervall**: Standardmäßig alle 3 Sekunden (konfigurierbar über `VISION_INTERVAL`)
- **Automatische Analyse**: Jedes Bild wird analysiert für Teilnehmer-Erkennung und Verhalten
- **Kontext-Updates**: Wichtige visuelle Informationen werden automatisch an das LLM gesendet

### Verhaltensanalyse

Der Bot analysiert kontinuierlich:
- **Teilnehmer-Tracking**: Wer ist anwesend, wer hat den Raum verlassen
- **Aktivitäts-Monitoring**: Wer spricht, wer zeigt Reaktionen
- **Engagement-Level**: Aktiv, passiv, abgelenkt, interessiert
- **Gruppendynamik**: Interaktionen zwischen Teilnehmern

### Moderation Tools

Der Bot hat Zugriff auf folgende Tools:
- `save_meeting_note`: Notizen während des Meetings speichern
- `update_speaker_timer`: Redezeit pro Sprecher tracken
- `track_topic`: Diskussionsthemen verfolgen
- `update_participant`: Teilnehmer-Informationen verwalten
- `analyze_behavior`: Verhaltensanalyse der Teilnehmer
- `get_visual_context`: Aktuelle visuelle Situation abfragen
- `generate_summary`: Zusammenfassungen generieren

## Anpassungen

### Screenshot-Bereich anpassen

Wenn du nur einen bestimmten Bereich des VRChat-Fensters erfassen möchtest:

```bash
export VRChat_WINDOW_REGION="(0, 0, 1920, 1080)"  # x, y, width, height
```

### System Prompt anpassen

Bearbeite die Funktion `create_moderation_system_prompt()` in `vrchat_moderator.py` um den Moderations-Stil anzupassen.

### Face Expressions anpassen

Bearbeite `create_vrchat_face_controller()` um zusätzliche Gesichtsausdrücke hinzuzufügen oder zu ändern.

## Troubleshooting

### Bot hört kein Audio

- Prüfe, ob VB-Cable-B Output als Input-Device korrekt konfiguriert ist
- Stelle sicher, dass VB-Cable-B Input als Standard-Ausgabegerät in Windows gesetzt ist
- Prüfe VRChat-Audio-Einstellungen

### Bot spricht nicht in VRChat

- Prüfe, ob VB-Cable-A Input als Output-Device korrekt konfiguriert ist
- Stelle sicher, dass VB-Cable-A als Mikrofon in VRChat gesetzt ist
- Prüfe OSC-Verbindung (Port 9000)

### Vision funktioniert nicht

- Stelle sicher, dass VRChat-Fenster sichtbar ist
- Prüfe, ob `pyautogui` installiert ist
- Bei Multi-Monitor-Setup: Passe `VRChat_WINDOW_REGION` an

### Speaker Diarization funktioniert nicht

- Stelle sicher, dass `resemblyzer` installiert ist
- Prüfe Audio-Qualität (zu viel Rauschen kann Probleme verursachen)

## Erweiterte Features

### PostgreSQL für bessere Performance

Für Produktionsumgebungen wird PostgreSQL empfohlen:

```python
# In vrchat_moderator.py
aiavatar_app = AIAvatar(
    # ...
    db_connection_str="postgresql://user:pass@localhost/aiavatar"
)
```

### Erweiterte Verhaltensanalyse

Die `analyze_meeting_scene()` Funktion kann erweitert werden mit:
- Computer Vision Models für detaillierte Verhaltensanalyse
- Objekt-Erkennung für spezifische Gesten
- Emotion-Erkennung basierend auf Avatar-Positionen

## Lizenz

Siehe Haupt-Lizenz von AIAvatarKit.
