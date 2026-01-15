# 🔧 .env Datei Setup - Schritt für Schritt

## Problem: API Key wird nicht gefunden

Wenn du diese Meldung siehst:
```
⚠️ API Key NICHT gesetzt!
```

Dann wird deine `.env` Datei nicht korrekt geladen.

---

## ✅ Lösung: Schritt für Schritt

### Schritt 1: Prüfe ob .env Datei existiert

```powershell
# Im Projektverzeichnis
cd "C:\Users\AI LAB VII\Desktop\temp ta\VR Assistant\AIavatarKIT\aiavatarkit"

# Prüfe ob .env existiert
Test-Path .env
```

**Sollte `True` zurückgeben.**

### Schritt 2: Erstelle .env Datei (falls nicht vorhanden)

```powershell
# Kopiere die Vorlage
Copy-Item ENV_VORLAGE.txt .env

# Oder erstelle manuell:
New-Item -Path .env -ItemType File
```

### Schritt 3: Fülle .env Datei aus

Öffne `.env` in einem Texteditor (Notepad, VS Code, etc.):

```
OPENAI_API_KEY=sk-dein-api-key-hier
VRChat_INPUT_DEVICE=16
VRChat_OUTPUT_DEVICE=13
OPENAI_TTS_MODEL=tts-1-hd
OPENAI_TTS_VOICE=alloy
VISION_INTERVAL=3.0
OSC_HOST=127.0.0.1
OSC_PORT=9000
ENABLE_FACE_CONTROLLER=true
```

**WICHTIG:** Ersetze `sk-dein-api-key-hier` mit deinem echten OpenAI API Key!

### Schritt 4: Installiere python-dotenv

```powershell
# Aktiviere venv
.\venv_moderator\Scripts\Activate.ps1

# Installiere python-dotenv
pip install python-dotenv
```

### Schritt 5: Prüfe ob .env geladen wird

```powershell
# Starte Bot
python vrchat_moderator.py
```

**Du solltest jetzt sehen:**
```
✓ .env Datei geladen: C:\Users\AI LAB VII\Desktop\temp ta\VR Assistant\AIavatarKIT\aiavatarkit\.env
✓ API Key gesetzt: sk-proj-...xxxx
```

**Falls nicht:**
```
⚠️ .env Datei nicht gefunden: ...
```

---

## 🔍 Troubleshooting

### Problem 1: ".env Datei nicht gefunden"

**Lösung:**
1. Prüfe ob `.env` im richtigen Verzeichnis ist (Projektverzeichnis)
2. Prüfe ob Datei wirklich `.env` heißt (nicht `.env.txt` oder ähnlich)
3. Windows Explorer: "Ansicht" → "Ausgeblendete Elemente" aktivieren

### Problem 2: "python-dotenv nicht installiert"

**Lösung:**
```powershell
.\venv_moderator\Scripts\Activate.ps1
pip install python-dotenv
```

### Problem 3: "API Key wird immer noch nicht gefunden"

**Lösung:**
1. Prüfe `.env` Datei:
   - Keine Leerzeichen um `=`
   - Keine Anführungszeichen um den Wert
   - Keine Kommentare in derselben Zeile

**Richtig:**
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Falsch:**
```
OPENAI_API_KEY = sk-proj-...  # Leerzeichen um =
OPENAI_API_KEY="sk-proj-..."  # Anführungszeichen
OPENAI_API_KEY=sk-proj-... # Kommentar
```

2. Prüfe ob API Key korrekt ist:
   ```powershell
   # Teste manuell
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
   ```

### Problem 4: "Bot beendet sich sofort"

**Ursache:** API Key fehlt → LLM kann nicht initialisiert werden → Bot beendet sich

**Lösung:**
1. Stelle sicher, dass API Key in `.env` gesetzt ist
2. Starte Bot neu
3. Prüfe Logs für Fehlermeldungen

---

## ✅ Korrekte venv Aktivierung

```powershell
# 1. Navigiere zum Projektverzeichnis
cd "C:\Users\AI LAB VII\Desktop\temp ta\VR Assistant\AIavatarKIT\aiavatarkit"

# 2. Aktiviere venv
.\venv_moderator\Scripts\Activate.ps1

# 3. Prüfe ob python-dotenv installiert ist
pip list | Select-String "dotenv"

# 4. Falls nicht, installiere es
pip install python-dotenv

# 5. Prüfe ob .env existiert
Test-Path .env

# 6. Starte Bot
python vrchat_moderator.py
```

---

## 📝 Checkliste

- [ ] `.env` Datei existiert im Projektverzeichnis
- [ ] `OPENAI_API_KEY` ist in `.env` gesetzt (ohne Anführungszeichen)
- [ ] `python-dotenv` ist installiert (`pip install python-dotenv`)
- [ ] venv ist aktiviert (`.\venv_moderator\Scripts\Activate.ps1`)
- [ ] Bot zeigt "✓ .env Datei geladen" beim Start
- [ ] Bot zeigt "✓ API Key gesetzt: sk-..." beim Start

---

## 🆘 Wenn nichts funktioniert

**Alternative: Umgebungsvariable setzen**

```powershell
# Temporär (nur für diese PowerShell-Session)
$env:OPENAI_API_KEY="sk-dein-api-key-hier"

# Dauerhaft (Windows)
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-dein-api-key-hier", "User")
```

**WICHTIG:** Starte PowerShell neu nach dauerhafter Setzung!
