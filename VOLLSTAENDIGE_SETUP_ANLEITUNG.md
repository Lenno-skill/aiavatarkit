# 🎯 VOLLSTÄNDIGE SETUP-ANLEITUNG - VRChat Meeting Moderator Bot

Diese Anleitung führt dich Schritt für Schritt durch **ALLE** notwendigen Konfigurationen für den VRChat Meeting Moderator Bot mit OpenAI TTS.

---

## 📋 CHECKLISTE - Was du brauchst

### ✅ Bereits erledigt:
- [x] Python 3.13.2 installiert
- [x] Virtuelle Umgebung erstellt (`venv_moderator`)
- [x] Dependencies installiert
- [x] VB-CABLE installiert
- [x] Audio-Geräte-Indizes gefunden (16 und 13)
- [x] Code für OpenAI TTS angepasst

### ⚠️ Noch zu erledigen:
- [ ] OpenAI API Key besorgen und setzen
- [ ] VRChat installieren und konfigurieren
- [ ] Kostenlosen Avatar finden und herunterladen
- [ ] Avatar in Unity konfigurieren (FaceOSC Parameter)
- [ ] VRChat OSC aktivieren
- [ ] Bot testen

---

## 🔑 SCHRITT 1: OpenAI API Key besorgen und setzen

### 1.1 API Key erstellen

1. **Gehe zu OpenAI:**
   - Website: https://platform.openai.com/
   - Klicke auf "Sign up" oder "Log in"

2. **API Key erstellen:**
   - Nach Login: Klicke auf dein Profilbild (oben rechts)
   - Wähle "View API keys"
   - Klicke auf "Create new secret key"
   - **WICHTIG:** Kopiere den Key sofort! Er wird nur einmal angezeigt.
   - Beispiel-Format: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **API Key setzen:**

   **Option A: Als Umgebungsvariable (PowerShell - temporär):**
   ```powershell
   $env:OPENAI_API_KEY="sk-dein-api-key-hier"
   ```

   **Option B: Als Umgebungsvariable (PowerShell - dauerhaft):**
   ```powershell
   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-dein-api-key-hier", "User")
   ```
   **WICHTIG:** Starte PowerShell neu nach dieser Änderung!

   **Option C: In .env Datei (EMPFOHLEN):**
   - Erstelle eine Datei namens `.env` im Projektverzeichnis
   - Kopiere den Inhalt von `.env.example` und fülle aus:
     ```
     OPENAI_API_KEY=sk-dein-api-key-hier
     VRChat_INPUT_DEVICE=16
     VRChat_OUTPUT_DEVICE=13
     OPENAI_TTS_MODEL=tts-1-hd
     OPENAI_TTS_VOICE=alloy
     ```

### 1.2 Verifikation

```powershell
# Teste ob API Key gesetzt ist:
echo $env:OPENAI_API_KEY
```

**Sollte deinen API Key zeigen (beginnt mit `sk-`).**

---

## 🎮 SCHRITT 2: VRChat installieren und konfigurieren

### 2.1 VRChat installieren

1. **Download:**
   - Website: https://hello.vrchat.com/
   - Klicke auf "Download VRChat"
   - Installiere VRChat (Desktop-Modus)

2. **Account erstellen:**
   - Erstelle einen Account für den Bot
   - **WICHTIG:** Notiere dir Username und Passwort!

3. **VRChat starten:**
   - Starte VRChat im Desktop-Modus
   - Logge dich mit dem Bot-Account ein

### 2.2 Audio-Einstellungen in VRChat

1. **VRChat öffnen**
2. **Settings → Audio:**
   - **Microphone:** Wähle "CABLE Input (VB-Audio Virtual Cable)"
   - **Speaker:** Standard (wird automatisch auf VB-Cable-B Input umgeleitet)

3. **Audio testen:**
   - Sprich in dein Mikrofon
   - Prüfe ob Audio ankommt

### 2.3 OSC aktivieren

1. **In VRChat:**
   - Settings → OSC
   - Aktiviere "Enable OSC"
   - **Port:** 9000 (Standard)
   - **Host:** 127.0.0.1 (Standard)

2. **Verifikation:**
   - OSC sollte "Enabled" anzeigen
   - Port sollte 9000 sein

---

## 👤 SCHRITT 3: Kostenlosen Avatar finden

### 3.1 Empfohlene Quellen für kostenlose Avatare

#### Option A: VRChat Avatar Worlds (Einfachste Methode) ⭐ EMPFOHLEN

1. **In VRChat:**
   - Öffne "Worlds"
   - Suche nach "Avatar" oder "Free Avatar"
   - Beliebte Worlds:
     - "Avatar Search" von AvatarSearch
     - "Free Avatar Worlds"
     - "Avatar Showcase"
     - "Avatar Testing"

2. **Avatar klonen:**
   - Gehe in ein Avatar-World
   - Klicke auf einen Avatar
   - Wähle "Clone Avatar"
   - Avatar wird zu deiner Favoriten-Liste hinzugefügt
   - **VORTEIL:** Keine Unity-Konfiguration nötig, wenn Avatar bereits FaceOSC hat!

#### Option B: Booth.pm (Viele kostenlose Avatare)

1. **Website:** https://booth.pm/
2. **Suche:**
   - Suche nach "VRChat Avatar"
   - Filter: "Free" aktivieren
   - Beliebte kostenlose Avatare:
     - **"Rexouium Base"** - Professionell, vielseitig, gut für Moderation
     - "VRoid" Avatare - Viele kostenlos verfügbar
     - "TDA Base" Avatare - Klassisch, professionell

3. **Download:**
   - Klicke auf Avatar
   - "Download" klicken
   - Unity-Package (.unitypackage) herunterladen

#### Option C: VRoid Hub (Anime-Style, viele kostenlos)

1. **Website:** https://hub.vroid.com/
2. **Suche:**
   - Filter: "VRChat" und "Free"
   - Viele professionelle Anime-Avatare verfügbar

#### Option D: Gumroad (Professionelle Avatare, teilweise kostenlos)

1. **Website:** https://gumroad.com/
2. **Suche:** "VRChat Avatar Free"

### 3.2 Empfohlene kostenlose Avatare (2024)

**Für professionelle Moderation empfehle ich:**

1. **"Rexouium Base"** (Booth.pm) ⭐ BESTE WAHL
   - Professionell, vielseitig
   - Gut für Business/Moderation
   - Kostenlos verfügbar
   - Link: https://booth.pm/de/items/xxxxx (Suche auf Booth.pm)

2. **"VRoid" Avatare**
   - Viele kostenlose Optionen
   - Professionell aussehend
   - Einfach zu konfigurieren

3. **"TDA Base" Avatare**
   - Klassisch, professionell
   - Viele kostenlose Varianten

### 3.3 Avatar herunterladen

**Wenn du einen Avatar gefunden hast:**

1. **Unity-Package (.unitypackage) herunterladen** (falls von Booth.pm/Gumroad)
2. **ODER Avatar in VRChat klonen** (falls aus Avatar-World)
3. **Speichere die Datei** (z.B. `avatar.unitypackage`)

---

## 🛠️ SCHRITT 4: Avatar in Unity konfigurieren

**⚠️ WICHTIG:** Dieser Schritt ist nur nötig, wenn du einen Avatar von Booth.pm/Gumroad heruntergeladen hast. Wenn du einen Avatar aus einem VRChat-World geklont hast, der bereits FaceOSC hat, kannst du diesen Schritt überspringen!

### 4.1 Unity installieren

1. **Download Unity Hub:**
   - Website: https://unity.com/download
   - Installiere Unity Hub

2. **Unity Version installieren:**
   - Öffne Unity Hub
   - "Installs" → "Add" → Wähle **Unity 2019.4.31f1** (LTS)
   - **WICHTIG:** Diese Version ist kompatibel mit VRChat SDK
   - Installiere mit "VRChat SDK" Support

3. **VRChat SDK installieren:**
   - Website: https://vrchat.com/download/sdk3
   - Lade "VRChat SDK 3" herunter
   - Speichere die Datei (z.B. `VRCSDK3-2023.xx.xx.xx.xx_xxxxx.unitypackage`)

### 4.2 Unity-Projekt erstellen

1. **Neues Projekt:**
   - Unity Hub → "New Project"
   - Template: "3D"
   - Name: "VRChatModeratorAvatar"
   - Erstelle Projekt

2. **VRChat SDK importieren:**
   - Assets → Import Package → Custom Package
   - Wähle die heruntergeladene VRChat SDK Datei
   - Importiere alles
   - **WICHTIG:** Folge allen Anweisungen im SDK

3. **Avatar importieren:**
   - Assets → Import Package → Custom Package
   - Wähle deinen Avatar (.unitypackage)
   - Importiere alles

### 4.3 FaceOSC Parameter hinzufügen

#### Schritt 1: Avatar in Scene öffnen

1. **Finde deinen Avatar:**
   - In "Project" Fenster: Suche nach deinem Avatar
   - Ziehe den Avatar in die Scene

2. **Avatar auswählen:**
   - Klicke auf den Avatar in der Scene
   - Im "Inspector" Fenster siehst du die Avatar-Komponente

#### Schritt 2: FaceOSC Parameter erstellen

1. **VRChat Avatar Descriptor öffnen:**
   - Wähle Avatar in Scene
   - Im Inspector: Finde "VRC Avatar Descriptor"
   - Klicke auf "Expressions Menu" oder "Parameters"

2. **Parameter hinzufügen:**
   - Klicke auf "Parameters" Tab
   - Klicke "+" um neuen Parameter hinzuzufügen
   - **Name:** `FaceOSC`
   - **Type:** `Int`
   - **Default Value:** `0`
   - **Saved:** ❌ (NICHT aktivieren)
   - **Synced:** ✅ (AKTIVIEREN)

3. **Parameter speichern:**
   - Klicke "Apply" oder "Save"

#### Schritt 3: FX Animator Controller konfigurieren

1. **Animator Controller öffnen:**
   - Finde "FX" Animator Controller (meist im Avatar-Ordner)
   - Doppelklick zum Öffnen

2. **FaceOSC Parameter hinzufügen:**
   - Im Animator: Klicke auf "Parameters" Tab (oben links)
   - Klicke "+" → "Int"
   - **Name:** `FaceOSC`

3. **States für Gesichtsausdrücke erstellen:**

   **Für jeden Gesichtsausdruck:**
   
   - Klicke rechts → "Create State" → "Empty"
   - **Name:** z.B. "Neutral", "Attentive", "Friendly", etc.
   - Wähle den State
   - Im Inspector: Füge "Set Int Parameter" hinzu
   - **Parameter:** `FaceOSC`
   - **Value:** 
     - Neutral: 0
     - Attentive: 1
     - Friendly: 2
     - Thinking: 3
     - Speaking: 4
     - Listening: 5

4. **Transitions erstellen:**

   - Wähle "Any State" (oder einen anderen State)
   - Rechtsklick → "Make Transition" → Wähle deinen State
   - Wähle die Transition (Pfeil)
   - Im Inspector: "Conditions"
   - Klicke "+" → Wähle `FaceOSC` → Setze Wert (z.B. `Equals` → `1` für Attentive)

5. **Wiederhole für alle Gesichtsausdrücke**

   **Zusammenfassung der Werte:**
   - 0 = Neutral
   - 1 = Attentive
   - 2 = Friendly
   - 3 = Thinking
   - 4 = Speaking
   - 5 = Listening

#### Schritt 4: Avatar testen

1. **VRChat SDK → Show Build Control Panel:**
   - Oben in Unity: "VRChat SDK" → "Show Build Control Panel"

2. **Build & Test:**
   - Klicke "Build & Test"
   - Avatar wird in VRChat geladen
   - Teste FaceOSC Parameter

### 4.4 Avatar hochladen

1. **In Unity:**
   - VRChat SDK → "Show Build Control Panel"
   - Klicke "Build & Publish for Windows"
   - Warte bis Upload fertig ist

2. **In VRChat:**
   - Gehe zu "Avatars"
   - Dein Avatar sollte jetzt verfügbar sein
   - Wähle ihn aus

---

## 🎯 SCHRITT 5: Finale Konfiguration

### 5.1 .env Datei erstellen (Empfohlen)

**Erstelle eine `.env` Datei im Projektverzeichnis:**

```
OPENAI_API_KEY=sk-dein-api-key-hier
VRChat_INPUT_DEVICE=16
VRChat_OUTPUT_DEVICE=13
OPENAI_TTS_MODEL=tts-1-hd
OPENAI_TTS_VOICE=alloy
VISION_INTERVAL=3.0
OSC_HOST=127.0.0.1
OSC_PORT=9000
```

**Oder kopiere `.env.example` und fülle aus:**
```powershell
Copy-Item .env.example .env
# Dann bearbeite .env und setze deinen API Key
```

### 5.2 Windows Sound-Einstellungen

1. **Windows Einstellungen → System → Sound:**
   - **Standard-Ausgabegerät:** "CABLE Input (VB-Audio Virtual Cable)"
   - **Standard-Eingabegerät:** "CABLE Output (VB-Audio Virtual Cable)"

2. **Verifikation:**
   - Spiele Musik ab
   - Sollte über VB-Cable hörbar sein

### 5.3 VRChat final konfigurieren

1. **Avatar auswählen:**
   - In VRChat: Gehe zu "Avatars"
   - Wähle deinen konfigurierten Avatar

2. **Audio prüfen:**
   - Settings → Audio
   - Mikrofon: "CABLE Input"
   - Teste Audio (sollte funktionieren)

3. **OSC prüfen:**
   - Settings → OSC
   - Sollte "Enabled" sein
   - Port: 9000

---

## 🚀 SCHRITT 6: Bot starten und testen

### 6.1 Bot starten

```powershell
# 1. Aktiviere virtuelle Umgebung
.\venv_moderator\Scripts\Activate.ps1

# 2. Stelle sicher, dass API Key gesetzt ist
echo $env:OPENAI_API_KEY

# 3. Starte Bot
python vrchat_moderator.py
```

### 6.2 Erwartete Ausgabe

```
INFO - VRChat Meeting Moderator Bot gestartet
INFO - VB-CABLE Geräte automatisch gefunden:
INFO -   Input-Device (Bot hört VRChat): [16] CABLE Output
INFO -   Output-Device (Bot spricht zu VRChat): [13] CABLE Input
INFO - Kontinuierliche Vision-Überwachung gestartet
INFO - Warte auf Meeting-Teilnehmer...
```

### 6.3 In VRChat testen

1. **Gehe in eine Welt mit anderen Teilnehmern**
2. **Sprich in VRChat:**
   - Bot sollte Audio empfangen
   - Bot sollte antworten (mit OpenAI TTS Stimme - professionell, englisch/deutsch)
   - Bot sollte Screenshots machen (alle 3 Sekunden)

3. **Face Expressions testen:**
   - Bot sollte Gesichtsausdrücke ändern
   - Prüfe ob FaceOSC Parameter sich ändern

---

## 🎨 OpenAI TTS Stimmen-Anpassung

### Verfügbare Stimmen

Du kannst die Stimme in `.env` Datei anpassen:

```bash
OPENAI_TTS_VOICE=alloy  # Ändere zu: echo, fable, onyx, nova, shimmer
```

**Stimmen-Beschreibung:**

- **`alloy`** ⭐ EMPFOHLEN - Neutral, vielseitig, professionell (gut für Moderation)
- **`echo`** - Männlich, klar, autoritär
- **`fable`** - Britisch, erzählend
- **`onyx`** - Tief, männlich, seriös
- **`nova`** - Weiblich, freundlich, warm
- **`shimmer`** - Weiblich, sanft, professionell

### Model-Anpassung

```bash
OPENAI_TTS_MODEL=tts-1-hd  # Ändere zu: tts-1 (schneller) oder tts-1-hd (bessere Qualität)
```

- **`tts-1`** - Schneller, günstiger
- **`tts-1-hd`** - Bessere Qualität, etwas langsamer

---

## ✅ FINALE CHECKLISTE

### Code & Konfiguration
- [x] Code für OpenAI TTS angepasst (automatisch erledigt)
- [ ] OpenAI API Key besorgt und gesetzt
- [ ] .env Datei erstellt und ausgefüllt

### VRChat Setup
- [ ] VRChat installiert
- [ ] VRChat Account erstellt
- [ ] Avatar gefunden und heruntergeladen/geklont
- [ ] Avatar in Unity konfiguriert (nur wenn nötig)
- [ ] FaceOSC Parameter hinzugefügt (nur wenn nötig)
- [ ] FX Animator Controller konfiguriert (nur wenn nötig)
- [ ] Avatar hochgeladen (nur wenn nötig)
- [ ] VRChat Audio konfiguriert (CABLE Input als Mikrofon)
- [ ] OSC aktiviert (Port 9000)

### System-Konfiguration
- [ ] Windows Sound: CABLE Input als Standard-Ausgabe
- [ ] Windows Sound: CABLE Output als Standard-Eingabe

### Testing
- [ ] Bot gestartet
- [ ] Audio-Verbindung funktioniert
- [ ] Bot spricht (OpenAI TTS)
- [ ] Vision-System funktioniert (Screenshots)
- [ ] Face Expressions funktionieren

---

## 🆘 TROUBLESHOOTING

### Problem: "OpenAI API Key nicht gefunden"
**Lösung:**
- Prüfe ob API Key gesetzt ist: `echo $env:OPENAI_API_KEY`
- Stelle sicher, dass `.env` Datei existiert und korrekt ist
- Starte PowerShell neu (falls dauerhafte Umgebungsvariable gesetzt wurde)

### Problem: "Bot spricht nicht"
**Lösung:**
- Prüfe: Ist OpenAI API Key korrekt?
- Prüfe: Ist TTS korrekt konfiguriert? (sollte automatisch sein)
- Prüfe: Windows Sound: CABLE Input als Standard-Ausgabe?
- Prüfe: VRChat Audio: CABLE Input als Mikrofon?

### Problem: "Face Expressions funktionieren nicht"
**Lösung:**
- Prüfe: Ist FaceOSC Parameter im Avatar?
- Prüfe: Ist OSC aktiviert in VRChat?
- Prüfe: Port 9000 korrekt?
- Prüfe: Avatar ausgewählt in VRChat?

### Problem: "Vision funktioniert nicht"
**Lösung:**
- Prüfe: Ist VRChat-Fenster sichtbar?
- Prüfe: Ist `pyautogui` installiert? (`pip list | grep pyautogui`)
- Bei Multi-Monitor: Setze `VRChat_WINDOW_REGION` in `.env`

### Problem: "Audio-Geräte nicht gefunden"
**Lösung:**
- Führe aus: `python find_and_set_audio_devices.py`
- Prüfe ob VB-CABLE installiert ist
- Setze manuell in `.env`: `VRChat_INPUT_DEVICE=16` und `VRChat_OUTPUT_DEVICE=13`

---

## 📝 WICHTIGE HINWEISE

### OpenAI TTS Kosten

- **Modell:** `tts-1` = $15 pro 1 Million Zeichen
- **Modell:** `tts-1-hd` = $30 pro 1 Million Zeichen
- **Geschätzte Kosten:** Ca. $0.015 pro 1000 Wörter

### Avatar ohne Unity-Konfiguration

Wenn du einen Avatar aus einem VRChat-World klonst, der bereits FaceOSC Parameter hat, musst du **KEINE** Unity-Konfiguration machen! Der Avatar funktioniert direkt.

### System Prompt anpassen

Du kannst den System Prompt in `vrchat_moderator.py` anpassen (Funktion `create_moderation_system_prompt()`), um den Moderations-Stil zu ändern.

---

## 🎉 FERTIG!

Nach erfolgreichem Setup:

1. ✅ Bot läuft mit OpenAI TTS (professionelle Stimme)
2. ✅ Unterstützt Englisch und Deutsch
3. ✅ Kontinuierliche Vision-Überwachung aktiv
4. ✅ Face Expressions funktionieren
5. ✅ Moderation Tools verfügbar

**Viel Erfolg mit deinem VRChat Meeting Moderator Bot! 🚀**
