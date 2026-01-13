# Schritt-für-Schritt Setup-Anleitung

## Schritt 1: Virtuelle Umgebung erstellen und Dependencies installieren

### Option A: Automatisch (Empfohlen)

Führe einfach das Setup-Script aus:

```cmd
setup_moderator_env.bat
```

Das Script macht automatisch:
1. ✅ Erstellt virtuelle Umgebung (`venv_moderator`)
2. ✅ Aktiviert sie
3. ✅ Installiert alle Dependencies

### Option B: Manuell

Falls das Script nicht funktioniert, kannst du es manuell machen:

```cmd
# 1. Erstelle virtuelle Umgebung
python -m venv venv_moderator

# 2. Aktiviere virtuelle Umgebung
venv_moderator\Scripts\activate.bat

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Installiere AIAvatarKit
pip install -e .

# 5. Installiere Moderator-Dependencies
pip install -r requirements_all.txt
```

## Schritt 2: Virtuelle Umgebung aktivieren

**WICHTIG:** Jedes Mal wenn du den Bot starten möchtest, musst du die venv aktivieren:

```cmd
venv_moderator\Scripts\activate.bat
```

Du erkennst, dass die venv aktiviert ist, wenn du `(venv_moderator)` am Anfang deiner Kommandozeile siehst:

```
(venv_moderator) PS C:\Users\AI LAB VII\Desktop\temp ta\VR Assistant\AIavatarKIT\aiavatarkit>
```

## Schritt 3: Audio-Geräte finden

Nachdem die venv aktiviert ist, kannst du die Audio-Geräte finden:

```cmd
# Stelle sicher, dass venv aktiviert ist!
venv_moderator\Scripts\activate.bat

# Dann führe aus:
python find_and_set_audio_devices.py
```

## Schritt 4: Was noch fehlt?

### ✅ Bereits erledigt (durch Setup-Script):
- Python installiert
- Virtuelle Umgebung erstellt
- Dependencies installiert

### ⚠️ Noch zu erledigen:

1. **OpenAI API Key** (ERFORDERLICH)
   - Gehe zu: https://platform.openai.com/api-keys
   - Erstelle einen neuen API Key
   - Setze als Umgebungsvariable:
     ```cmd
     set OPENAI_API_KEY=sk-dein-api-key-hier
     ```

2. **VB-CABLE** (ERFORDERLICH - du hast es bereits!)
   - ✅ Installiert (haben wir gesehen)
   - ⚠️ Audio-Geräte-Indizes finden (machst du in Schritt 3)

3. **VOICEVOX** (Optional, aber empfohlen)
   - Download: https://voicevox.hiroshiba.jp/
   - Installiere und starte VOICEVOX
   - Standard-Port: `http://127.0.0.1:50021`

4. **VRChat** (ERFORDERLICH)
   - Installiere VRChat (Desktop-Modus)
   - Erstelle Account für Bot
   - Konfiguriere Avatar (FaceOSC Parameter)
   - Aktiviere OSC (Port 9000)

## Häufige Probleme

### Problem: "No module named 'httpx'"
**Lösung:** 
- Stelle sicher, dass die venv aktiviert ist
- Führe aus: `pip install -r requirements_all.txt`

### Problem: "Python nicht gefunden"
**Lösung:**
- Prüfe ob Python im PATH ist: `python --version`
- Falls nicht: Installiere Python neu und aktiviere "Add Python to PATH"

### Problem: "Virtuelle Umgebung kann nicht aktiviert werden"
**Lösung:**
- Prüfe ob `venv_moderator` Ordner existiert
- Falls nicht: Führe `python -m venv venv_moderator` aus
- Bei PowerShell: Führe `venv_moderator\Scripts\Activate.ps1` aus (nicht .bat)

## Nächste Schritte

Nach erfolgreichem Setup:

1. ✅ Virtuelle Umgebung aktivieren
2. ✅ Audio-Geräte finden: `python find_and_set_audio_devices.py`
3. ✅ OpenAI API Key setzen
4. ✅ Bot starten: `python vrchat_moderator.py`
