# 📋 DETAILLIERTER AKTIONSPLAN - VRChat AIAvatar Bot Setup

**Status:** ✅ Code ist fertig | ⚠️ Konfiguration & Setup noch nötig

Dieses Dokument führt dich Schritt für Schritt durch **ALLE** noch notwendigen Schritte, um deinen AIAvatar Bot in VRChat zum Laufen zu bringen.

---

## 🎯 ÜBERSICHT - Was noch zu tun ist

### ✅ Bereits erledigt:
- [x] Python 3.13.2 installiert
- [x] Virtuelle Umgebung erstellt (`venv_moderator`)
- [x] Alle Dependencies installiert
- [x] Code für OpenAI TTS angepasst
- [x] Audio-Geräte-Indizes gefunden (16 und 13)
- [x] VB-CABLE installiert

### ⚠️ Noch zu erledigen (in dieser Reihenfolge):
1. [ ] **OpenAI API Key besorgen und konfigurieren**
2. [ ] **VRChat installieren und Account erstellen**
3. [ ] **Kostenlosen Avatar finden und herunterladen**
4. [ ] **Avatar in Unity konfigurieren** (FaceOSC Parameter) ⚠️ **OPTIONAL**
5. [ ] **Avatar in VRChat hochladen** (nur wenn Unity-Konfiguration nötig)
6. [ ] **VRChat Audio & OSC konfigurieren**
7. [ ] **Windows Sound-Einstellungen anpassen**
8. [ ] **Bot starten und testen**

**Geschätzte Zeit:** 
- **Ohne FaceOSC:** 1-2 Stunden
- **Mit FaceOSC (Unity-Setup):** 2-4 Stunden

**⚠️ WICHTIG:** FaceOSC ist **OPTIONAL**! Der Bot funktioniert auch ohne Gesichtsausdrücke. Du kannst später jederzeit FaceOSC hinzufügen.

---

## 📝 SCHRITT 1: OpenAI API Key besorgen und konfigurieren

**Zeitaufwand:** 10-15 Minuten  
**Schwierigkeit:** ⭐ Einfach

### 1.1 OpenAI Account erstellen (falls noch nicht vorhanden)

1. **Gehe zu OpenAI:**
   - Öffne deinen Browser
   - Gehe zu: https://platform.openai.com/
   - Klicke auf "Sign up" (Registrieren) oder "Log in" (Anmelden)

2. **Account erstellen:**
   - Folge den Anweisungen
   - Bestätige deine E-Mail-Adresse
   - **WICHTIG:** Du brauchst eine gültige Kreditkarte für API-Zugang

### 1.2 API Key erstellen

1. **Nach Login:**
   - Klicke auf dein Profilbild (oben rechts)
   - Wähle "View API keys" aus dem Dropdown-Menü

2. **Neuen Key erstellen:**
   - Klicke auf den Button "Create new secret key"
   - Gib einen Namen ein (z.B. "VRChat Bot")
   - Klicke "Create secret key"
   - **⚠️ WICHTIG:** Kopiere den Key SOFORT! Er wird nur einmal angezeigt.
   - Der Key sieht so aus: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Key sicher speichern:**
   - Kopiere den Key in einen Texteditor
   - Speichere ihn sicher (z.B. in einem Passwort-Manager)

### 1.3 API Key in .env Datei setzen

**Option A: .env Datei erstellen (EMPFOHLEN)**

1. **Gehe zum Projektverzeichnis:**
   ```powershell
   cd "C:\Users\AI LAB VII\Desktop\temp ta\VR Assistant\AIavatarKIT\aiavatarkit"
   ```

2. **Erstelle .env Datei:**
   ```powershell
   # Kopiere die Vorlage
   Copy-Item ENV_VORLAGE.txt .env
   
   # Oder erstelle manuell:
   New-Item -Path .env -ItemType File
   ```

3. **Öffne .env in einem Texteditor:**
   ```powershell
   notepad .env
   ```

4. **Fülle die Datei aus:**
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
   
   **WICHTIG:** Ersetze `sk-dein-api-key-hier` mit deinem echten API Key!

5. **Speichere die Datei** (Strg+S)

**Option B: Als Umgebungsvariable setzen (temporär)**

```powershell
$env:OPENAI_API_KEY="sk-dein-api-key-hier"
```

**⚠️ Nachteil:** Muss bei jedem neuen PowerShell-Fenster neu gesetzt werden.

**Option C: Als permanente Umgebungsvariable (Windows)**

```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-dein-api-key-hier", "User")
```

**⚠️ WICHTIG:** Starte PowerShell neu nach dieser Änderung!

### 1.4 Verifikation

```powershell
# Teste ob API Key gesetzt ist:
echo $env:OPENAI_API_KEY

# Sollte deinen API Key zeigen (beginnt mit sk-)
```

**✅ Checkliste Schritt 1:**
- [ ] OpenAI Account erstellt
- [ ] API Key erstellt und kopiert
- [ ] .env Datei erstellt
- [ ] API Key in .env eingetragen
- [ ] Verifikation erfolgreich

---

## 🎮 SCHRITT 2: VRChat installieren und Account erstellen

**Zeitaufwand:** 20-30 Minuten  
**Schwierigkeit:** ⭐ Einfach

### 2.1 VRChat herunterladen

1. **Gehe zu VRChat:**
   - Öffne Browser
   - Gehe zu: https://hello.vrchat.com/
   - Klicke auf "Download VRChat"

2. **Installation:**
   - Lade den Installer herunter
   - Führe den Installer aus
   - Folge den Installations-Anweisungen
   - **WICHTIG:** Installiere im "Desktop-Modus" (nicht VR-Modus)

### 2.2 VRChat Account erstellen

1. **VRChat starten:**
   - Öffne VRChat
   - Beim ersten Start: Klicke "Create Account"

2. **Account-Daten eingeben:**
   - **Username:** Wähle einen Namen (z.B. "AIAvatarBot")
   - **E-Mail:** Deine E-Mail-Adresse
   - **Passwort:** Sicheres Passwort
   - **Geburtsdatum:** Muss 18+ sein

3. **E-Mail bestätigen:**
   - Prüfe dein E-Mail-Postfach
   - Klicke auf den Bestätigungslink

4. **Account-Daten notieren:**
   - **Username:** _________________
   - **Passwort:** _________________
   - **E-Mail:** _________________

### 2.3 VRChat zum ersten Mal starten

1. **Login:**
   - Starte VRChat
   - Logge dich mit deinem Account ein

2. **Tutorial überspringen (optional):**
   - Du kannst das Tutorial überspringen, da du den Bot im Desktop-Modus verwendest

3. **Verifikation:**
   - Du solltest im VRChat-Hauptmenü sein
   - Dein Avatar sollte sichtbar sein (Standard-Avatar)

**✅ Checkliste Schritt 2:**
- [ ] VRChat heruntergeladen
- [ ] VRChat installiert
- [ ] Account erstellt
- [ ] E-Mail bestätigt
- [ ] Account-Daten notiert
- [ ] VRChat erfolgreich gestartet

---

## 👤 SCHRITT 3: Kostenlosen Avatar finden und herunterladen

**Zeitaufwand:** 30-60 Minuten  
**Schwierigkeit:** ⭐⭐ Mittel

### 3.1 Option A: Avatar aus VRChat-World klonen (EINFACHSTE METHODE) ⭐ EMPFOHLEN

**Vorteil:** Keine Unity-Konfiguration nötig, wenn Avatar bereits FaceOSC hat!

1. **In VRChat:**
   - Gehe zu "Worlds" (oben im Menü)
   - Suche nach "Avatar" oder "Free Avatar"

2. **Beliebte Avatar-Worlds:**
   - "Avatar Search" von AvatarSearch
   - "Free Avatar Worlds"
   - "Avatar Showcase"
   - "Avatar Testing"

3. **Avatar-World betreten:**
   - Klicke auf ein World
   - Klicke "Go" oder "Enter"

4. **Avatar klonen:**
   - Gehe zu einem Avatar (klicke darauf)
   - Klicke auf "Clone Avatar" oder "Favor Avatar"
   - Avatar wird zu deiner Favoriten-Liste hinzugefügt

5. **Avatar auswählen:**
   - Gehe zu "Avatars" (oben im Menü)
   - Finde deinen geklonten Avatar
   - Klicke darauf, um ihn auszuwählen

6. **FaceOSC prüfen:**
   - **WICHTIG:** Nicht alle Avatare haben FaceOSC Parameter!
   - Wenn der Avatar FaceOSC hat, kannst du **Schritt 4 überspringen**!
   - Wenn nicht, musst du den Avatar in Unity konfigurieren (Schritt 4)

**✅ Wenn Avatar FaceOSC hat:**
- [ ] Avatar geklont
- [ ] Avatar ausgewählt
- [ ] FaceOSC Parameter vorhanden
- → **ÜBERSPRINGE SCHRITT 4** und gehe zu Schritt 5

**⚠️ Wenn Avatar KEIN FaceOSC hat:**
- [ ] Avatar geklont
- [ ] Avatar ausgewählt
- [ ] FaceOSC Parameter fehlt
- → **OPTION 1:** Bot OHNE FaceOSC nutzen (funktioniert perfekt, nur ohne Gesichtsausdrücke)
- → **OPTION 2:** **FORTFAHREN MIT SCHRITT 4** (Unity-Konfiguration für FaceOSC)

**💡 TIPP:** Du kannst den Bot **erstmal OHNE FaceOSC** testen und später FaceOSC hinzufügen, wenn du möchtest!

### 3.2 Option B: Avatar von Booth.pm herunterladen

1. **Gehe zu Booth.pm:**
   - Browser öffnen
   - Gehe zu: https://booth.pm/

2. **Suche nach Avatar:**
   - Suche nach "VRChat Avatar"
   - Filter: "Free" aktivieren
   - Sortiere nach "Popular" oder "New"

3. **Empfohlene kostenlose Avatare:**
   - **"Rexouium Base"** - Professionell, vielseitig ⭐ BESTE WAHL
   - "VRoid" Avatare - Viele kostenlos
   - "TDA Base" Avatare - Klassisch, professionell

4. **Avatar herunterladen:**
   - Klicke auf einen Avatar
   - Klicke "Download"
   - Wähle "Unity Package" (.unitypackage)
   - Speichere die Datei (z.B. `avatar.unitypackage`)

5. **Datei speichern:**
   - Speichere die .unitypackage Datei in einem Ordner (z.B. `C:\Users\AI LAB VII\Desktop\VRChat Avatars\`)

**✅ Checkliste Schritt 3:**
- [ ] Avatar gefunden (aus World geklont ODER von Booth.pm heruntergeladen)
- [ ] Avatar-Datei gespeichert (falls von Booth.pm)
- [ ] FaceOSC Status geprüft (hat Avatar FaceOSC?)

---

## 🛠️ SCHRITT 4: Avatar in Unity konfigurieren (OPTIONAL - nur für FaceOSC!)

**Zeitaufwand:** 1-2 Stunden  
**Schwierigkeit:** ⭐⭐⭐ Fortgeschritten

**⚠️ WICHTIG:** Dieser Schritt ist **KOMPLETT OPTIONAL**!

**Du kannst diesen Schritt überspringen, wenn:**
- ✅ Du den Bot **ohne Gesichtsausdrücke** nutzen möchtest (funktioniert perfekt!)
- ✅ Dein Avatar bereits FaceOSC hat (dann überspringe diesen Schritt)

**Du musst diesen Schritt nur machen, wenn:**
- Du einen Avatar von Booth.pm/Gumroad heruntergeladen hast
- UND du FaceOSC-Gesichtsausdrücke haben möchtest
- UND dein Avatar KEIN FaceOSC Parameter hat

**💡 EMPFEHLUNG:** Teste den Bot **erstmal OHNE FaceOSC**. Du kannst später jederzeit FaceOSC hinzufügen!

### 4.1 Unity Hub installieren

1. **Download Unity Hub:**
   - Browser öffnen
   - Gehe zu: https://unity.com/download
   - Klicke "Download Unity Hub"

2. **Unity Hub installieren:**
   - Führe den Installer aus
   - Folge den Anweisungen
   - Starte Unity Hub

### 4.2 Unity Version installieren

1. **In Unity Hub:**
   - Klicke auf "Installs" (oben)
   - Klicke "Add" oder "Install Editor"

2. **Version wählen:**
   - Wähle **Unity 2019.4.31f1** (LTS Version)
   - **WICHTIG:** Diese Version ist kompatibel mit VRChat SDK 3
   - Klicke "Install"

3. **Module auswählen:**
   - Wähle "Windows Build Support" (IL2CPP)
   - Klicke "Install"
   - **Warte bis Installation fertig ist** (kann 10-20 Minuten dauern)

### 4.3 VRChat SDK herunterladen

1. **Gehe zu VRChat SDK:**
   - Browser öffnen
   - Gehe zu: https://vrchat.com/download/sdk3
   - Logge dich mit deinem VRChat Account ein

2. **SDK herunterladen:**
   - Klicke "Download VRChat SDK 3"
   - Speichere die Datei (z.B. `VRCSDK3-2023.xx.xx.xx.xx_xxxxx.unitypackage`)
   - **WICHTIG:** Notiere dir den Speicherort!

### 4.4 Unity-Projekt erstellen

1. **In Unity Hub:**
   - Klicke "New Project"
   - Template: "3D"
   - Projektname: "VRChatModeratorAvatar"
   - Speicherort: Wähle einen Ordner (z.B. `C:\Users\AI LAB VII\Desktop\Unity Projects\`)
   - Klicke "Create project"

2. **Warte bis Projekt geladen ist:**
   - Unity Editor öffnet sich
   - Kann einige Minuten dauern

### 4.5 VRChat SDK importieren

1. **In Unity Editor:**
   - Oben im Menü: "Assets" → "Import Package" → "Custom Package..."
   - Wähle die heruntergeladene VRChat SDK Datei
   - Klicke "Open"

2. **Import-Dialog:**
   - Stelle sicher, dass ALLES ausgewählt ist
   - Klicke "Import"
   - **WICHTIG:** Folge allen Anweisungen im SDK (z.B. "Accept" bei Lizenz)

3. **Verifikation:**
   - Im Menü sollte "VRChat SDK" erscheinen
   - Im "Project" Fenster sollte ein "VRCSDK" Ordner sichtbar sein

### 4.6 Avatar importieren

1. **In Unity Editor:**
   - "Assets" → "Import Package" → "Custom Package..."
   - Wähle deine Avatar .unitypackage Datei
   - Klicke "Open"

2. **Import-Dialog:**
   - Stelle sicher, dass ALLES ausgewählt ist
   - Klicke "Import"
   - Warte bis Import fertig ist

3. **Avatar in Scene hinzufügen:**
   - Im "Project" Fenster: Suche nach deinem Avatar (meist im "Assets" Ordner)
   - Ziehe den Avatar in die "Hierarchy" (links)
   - Der Avatar sollte jetzt in der Scene sichtbar sein

### 4.7 FaceOSC Parameter hinzufügen

#### Schritt 4.7.1: Avatar auswählen

1. **In Unity:**
   - Klicke auf den Avatar in der "Hierarchy"
   - Im "Inspector" Fenster (rechts) siehst du die Avatar-Komponenten

#### Schritt 4.7.2: VRChat Avatar Descriptor öffnen

1. **Im Inspector:**
   - Finde "VRC Avatar Descriptor" Komponente
   - Klicke darauf, um sie zu erweitern

2. **Parameters öffnen:**
   - Suche nach "Expressions Menu" oder "Parameters"
   - Klicke auf "Parameters" Tab

#### Schritt 4.7.3: FaceOSC Parameter erstellen

1. **Parameter hinzufügen:**
   - Klicke auf das "+" Symbol (neben "Parameters")
   - Wähle "Int" (Integer)

2. **Parameter konfigurieren:**
   - **Name:** `FaceOSC`
   - **Type:** `Int` (sollte bereits ausgewählt sein)
   - **Default Value:** `0`
   - **Saved:** ❌ (NICHT aktivieren - Checkbox leer lassen)
   - **Synced:** ✅ (AKTIVIEREN - Checkbox ankreuzen)

3. **Speichern:**
   - Klicke "Apply" oder "Save" (falls vorhanden)

#### Schritt 4.7.4: FX Animator Controller konfigurieren

1. **Animator Controller finden:**
   - Im "Project" Fenster: Suche nach "FX" Animator Controller
   - Meist im Avatar-Ordner (z.B. "Assets/AvatarName/FX.controller")
   - Doppelklick zum Öffnen

2. **Animator Window öffnen:**
   - Der Animator sollte sich in einem neuen Tab öffnen
   - Du siehst States (Rechtecke) und Transitions (Pfeile)

3. **FaceOSC Parameter hinzufügen:**
   - Im Animator: Klicke auf "Parameters" Tab (oben links)
   - Klicke "+" → "Int"
   - **Name:** `FaceOSC`

4. **States für Gesichtsausdrücke erstellen:**

   **Für jeden Gesichtsausdruck:**
   
   a. **State erstellen:**
      - Rechtsklick im Animator → "Create State" → "Empty"
      - **Name:** z.B. "Neutral", "Attentive", "Friendly", "Thinking", "Speaking", "Listening"
   
   b. **State konfigurieren:**
      - Klicke auf den State (Rechteck)
      - Im Inspector (rechts): Füge "Set Int Parameter" hinzu
      - **Parameter:** `FaceOSC`
      - **Value:** 
        - Neutral: `0`
        - Attentive: `1`
        - Friendly: `2`
        - Thinking: `3`
        - Speaking: `4`
        - Listening: `5`

5. **Transitions erstellen:**

   **Für jeden State:**
   
   a. **Transition erstellen:**
      - Wähle "Any State" (oder einen anderen State)
      - Rechtsklick → "Make Transition" → Wähle deinen State
   
   b. **Transition konfigurieren:**
      - Klicke auf die Transition (Pfeil)
      - Im Inspector: "Conditions"
      - Klicke "+" → Wähle `FaceOSC` → Setze Wert
      - Beispiel für "Attentive":
        - Parameter: `FaceOSC`
        - Condition: `Equals`
        - Value: `1`

6. **Wiederhole für alle Gesichtsausdrücke:**

   **Zusammenfassung der Werte:**
   - `0` = Neutral
   - `1` = Attentive
   - `2` = Friendly
   - `3` = Thinking
   - `4` = Speaking
   - `5` = Listening

#### Schritt 4.7.5: Avatar testen

1. **VRChat SDK → Show Build Control Panel:**
   - Oben in Unity: "VRChat SDK" → "Show Build Control Panel"
   - Ein neues Fenster öffnet sich

2. **Build & Test:**
   - Klicke "Build & Test"
   - Warte bis Build fertig ist
   - VRChat öffnet sich automatisch
   - Avatar wird geladen

3. **FaceOSC testen:**
   - In VRChat: Prüfe ob Avatar korrekt angezeigt wird
   - **Hinweis:** FaceOSC wird erst funktionieren, wenn der Bot läuft

### 4.8 Avatar hochladen

1. **In Unity:**
   - VRChat SDK → "Show Build Control Panel"
   - Klicke "Build & Publish for Windows"
   - Warte bis Upload fertig ist

2. **In VRChat:**
   - Gehe zu "Avatars"
   - Dein Avatar sollte jetzt verfügbar sein
   - Wähle ihn aus

**✅ Checkliste Schritt 4:**
- [ ] Unity Hub installiert
- [ ] Unity 2019.4.31f1 installiert
- [ ] VRChat SDK heruntergeladen
- [ ] Unity-Projekt erstellt
- [ ] VRChat SDK importiert
- [ ] Avatar importiert
- [ ] FaceOSC Parameter hinzugefügt
- [ ] FX Animator Controller konfiguriert
- [ ] Avatar getestet
- [ ] Avatar hochgeladen

---

## 🎮 SCHRITT 5: VRChat Audio & OSC konfigurieren

**Zeitaufwand:** 10-15 Minuten  
**Schwierigkeit:** ⭐ Einfach

### 5.1 VRChat Audio-Einstellungen

1. **VRChat öffnen:**
   - Starte VRChat
   - Logge dich ein

2. **Settings öffnen:**
   - Klicke auf das Zahnrad-Symbol (oben rechts)
   - Oder: Drücke ESC → "Settings"

3. **Audio-Einstellungen:**
   - Gehe zu "Audio" Tab
   - **Microphone:** Wähle "CABLE Input (VB-Audio Virtual Cable)"
   - **Speaker:** Standard (wird automatisch auf VB-Cable-B Input umgeleitet)

4. **Audio testen:**
   - Sprich in dein Mikrofon
   - Prüfe ob Audio ankommt (grüner Balken sollte sich bewegen)

### 5.2 OSC aktivieren

1. **In VRChat Settings:**
   - Gehe zu "OSC" Tab
   - Aktiviere "Enable OSC" (Checkbox ankreuzen)
   - **Port:** `9000` (Standard)
   - **Host:** `127.0.0.1` (Standard)

2. **Verifikation:**
   - OSC sollte "Enabled" anzeigen
   - Port sollte `9000` sein
   - Status sollte "Connected" oder "Ready" sein

### 5.3 Avatar auswählen

1. **In VRChat:**
   - Gehe zu "Avatars" (oben im Menü)
   - Wähle deinen konfigurierten Avatar aus
   - Avatar sollte jetzt sichtbar sein

**✅ Checkliste Schritt 5:**
- [ ] VRChat Audio konfiguriert (CABLE Input als Mikrofon)
- [ ] OSC aktiviert (Port 9000)
- [ ] Avatar ausgewählt

---

## 🔊 SCHRITT 6: Windows Sound-Einstellungen anpassen

**Zeitaufwand:** 5 Minuten  
**Schwierigkeit:** ⭐ Einfach

### 6.1 Windows Sound-Einstellungen öffnen

1. **Windows Settings:**
   - Drücke `Windows + I` (Einstellungen öffnen)
   - Oder: Rechtsklick auf Lautsprecher-Symbol → "Sound settings"

2. **Sound-Einstellungen:**
   - Gehe zu "System" → "Sound"
   - Oder direkt: `ms-settings:sound`

### 6.2 Standard-Ausgabegerät setzen

1. **Ausgabegerät:**
   - Unter "Output": Wähle "CABLE Input (VB-Audio Virtual Cable)"
   - **WICHTIG:** Das ist das Gerät, über das der Bot spricht

2. **Verifikation:**
   - Spiele Musik ab (z.B. YouTube)
   - Audio sollte über VB-CABLE laufen

### 6.3 Standard-Eingabegerät setzen (optional)

1. **Eingabegerät:**
   - Unter "Input": Wähle "CABLE Output (VB-Audio Virtual Cable)"
   - **Hinweis:** Wird normalerweise automatisch vom Bot verwendet

### 6.4 Verifikation

1. **Audio testen:**
   - Spiele Musik ab
   - Prüfe ob Audio über VB-CABLE läuft

**✅ Checkliste Schritt 6:**
- [ ] Windows Sound-Einstellungen geöffnet
- [ ] Standard-Ausgabegerät auf "CABLE Input" gesetzt
- [ ] Audio-Verifikation erfolgreich

---

## 🚀 SCHRITT 7: Bot starten und testen

**Zeitaufwand:** 10-15 Minuten  
**Schwierigkeit:** ⭐ Einfach

### 7.1 Vorbereitung

1. **Stelle sicher, dass alles konfiguriert ist:**
   - [ ] OpenAI API Key in .env gesetzt
   - [ ] VRChat läuft
   - [ ] Avatar ausgewählt
   - [ ] Audio & OSC konfiguriert
   - [ ] Windows Sound-Einstellungen angepasst

2. **VRChat starten:**
   - Starte VRChat
   - Logge dich ein
   - Gehe in eine Welt (z.B. "The Great Pug" oder "Black Cat")

### 7.2 Bot starten

1. **PowerShell öffnen:**
   - Drücke `Windows + X`
   - Wähle "Windows PowerShell" oder "Terminal"

2. **Zum Projektverzeichnis navigieren:**
   ```powershell
   cd "C:\Users\AI LAB VII\Desktop\temp ta\VR Assistant\AIavatarKIT\aiavatarkit"
   ```

3. **Virtuelle Umgebung aktivieren:**
   ```powershell
   .\venv_moderator\Scripts\Activate.ps1
   ```

4. **API Key prüfen (falls nicht in .env):**
   ```powershell
   echo $env:OPENAI_API_KEY
   ```
   **Sollte deinen API Key zeigen (beginnt mit sk-)**

5. **Bot starten:**
   ```powershell
   python vrchat_moderator.py
   ```

### 7.3 Erwartete Ausgabe

```
INFO - VRChat Meeting Moderator Bot gestartet
INFO - VB-CABLE Geräte automatisch gefunden:
INFO -   Input-Device (Bot hört VRChat): [16] CABLE Output
INFO -   Output-Device (Bot spricht zu VRChat): [13] CABLE Input
INFO - Kontinuierliche Vision-Überwachung gestartet
INFO - Warte auf Meeting-Teilnehmer...
```

### 7.4 Bot testen

1. **In VRChat:**
   - Sprich in dein Mikrofon
   - Bot sollte Audio empfangen

2. **Bot-Antwort prüfen:**
   - Bot sollte mit OpenAI TTS Stimme antworten
   - Stimme sollte professionell klingen (englisch/deutsch)

3. **Face Expressions prüfen:**
   - Bot sollte Gesichtsausdrücke ändern
   - Prüfe ob FaceOSC Parameter sich ändern (in VRChat)

4. **Vision-System prüfen:**
   - Bot macht alle 3 Sekunden Screenshots
   - Prüfe Logs für "Vision-Update" Nachrichten

### 7.5 Häufige Probleme und Lösungen

**Problem: "OpenAI API Key nicht gefunden"**
- **Lösung:** Prüfe ob .env Datei existiert und API Key korrekt ist
- **Lösung:** Setze Umgebungsvariable: `$env:OPENAI_API_KEY="sk-..."`

**Problem: "Bot spricht nicht"**
- **Lösung:** Prüfe Windows Sound: CABLE Input als Standard-Ausgabe?
- **Lösung:** Prüfe VRChat Audio: CABLE Input als Mikrofon?
- **Lösung:** Prüfe ob OpenAI API Key korrekt ist

**Problem: "Face Expressions funktionieren nicht"**
- **Hinweis:** Face Expressions sind OPTIONAL! Der Bot funktioniert auch ohne.
- **Lösung:** Prüfe ob OSC aktiviert ist (Port 9000) - nur nötig für FaceOSC
- **Lösung:** Prüfe ob FaceOSC Parameter im Avatar vorhanden ist
- **Lösung:** Prüfe ob Avatar ausgewählt ist
- **Lösung:** Prüfe ob `ENABLE_FACE_CONTROLLER=true` in .env gesetzt ist (Standard: aktiviert)

**Problem: "Audio-Geräte nicht gefunden"**
- **Lösung:** Führe aus: `python find_and_set_audio_devices.py`
- **Lösung:** Prüfe ob VB-CABLE installiert ist
- **Lösung:** Setze manuell in .env: `VRChat_INPUT_DEVICE=16` und `VRChat_OUTPUT_DEVICE=13`

**✅ Checkliste Schritt 7:**
- [ ] Bot gestartet
- [ ] Keine Fehler in der Ausgabe
- [ ] Audio-Verbindung funktioniert
- [ ] Bot spricht (OpenAI TTS)
- [ ] Vision-System funktioniert
- [ ] **OPTIONAL:** Face Expressions funktionieren (nur wenn FaceOSC aktiviert)

---

## 🎉 FERTIG!

**Herzlichen Glückwunsch!** Dein VRChat AIAvatar Bot sollte jetzt funktionieren!

### Was funktioniert jetzt:

✅ **Bot läuft mit OpenAI TTS** (professionelle Stimme, Englisch/Deutsch)  
✅ **Kontinuierliche Vision-Überwachung** (Screenshots alle 3 Sekunden)  
✅ **Moderation Tools** (Meeting Notes, Speaker Timer, etc.)  
✅ **Speaker Diarization** (erkennt verschiedene Sprecher)  
✅ **OPTIONAL: Face Expressions** (Avatar zeigt Emotionen - nur wenn FaceOSC aktiviert)

### Nächste Schritte (optional):

1. **System Prompt anpassen:**
   - Öffne `vrchat_moderator.py`
   - Finde Funktion `create_moderation_system_prompt()`
   - Passe den Moderations-Stil an

2. **Stimme anpassen:**
   - Ändere in `.env`: `OPENAI_TTS_VOICE=alloy` zu einer anderen Stimme
   - Optionen: `echo`, `fable`, `onyx`, `nova`, `shimmer`

3. **Vision-Intervall anpassen:**
   - Ändere in `.env`: `VISION_INTERVAL=3.0` zu einem anderen Wert (z.B. `5.0`)

---

## 📞 HILFE & SUPPORT

### Dokumentation:
- **Vollständige Anleitung:** `VOLLSTAENDIGE_SETUP_ANLEITUNG.md`
- **Quick Start:** `QUICK_START.md`
- **Schritt-für-Schritt:** `SETUP_SCHRITT_FUER_SCHRITT.md`

### Troubleshooting:
- Siehe "Häufige Probleme" in Schritt 7
- Prüfe Logs für Fehlermeldungen
- Stelle sicher, dass alle Dependencies installiert sind

### Kosten:
- **OpenAI TTS:** Ca. $0.015 pro 1000 Wörter (tts-1-hd)
- **OpenAI API:** Abhängig von Modell (GPT-4o empfohlen)

---

## ✅ FINALE CHECKLISTE

### Setup:
- [ ] OpenAI API Key besorgt und gesetzt
- [ ] VRChat installiert und Account erstellt
- [ ] Avatar gefunden und konfiguriert
- [ ] Unity Setup (falls nötig) abgeschlossen
- [ ] FaceOSC Parameter hinzugefügt
- [ ] Avatar hochgeladen
- [ ] VRChat Audio & OSC konfiguriert
- [ ] Windows Sound-Einstellungen angepasst

### Testing:
- [ ] Bot gestartet
- [ ] Audio-Verbindung funktioniert
- [ ] Bot spricht (OpenAI TTS)
- [ ] Face Expressions funktionieren
- [ ] Vision-System funktioniert
- [ ] Moderation Tools funktionieren

**Viel Erfolg mit deinem VRChat Meeting Moderator Bot! 🚀**
