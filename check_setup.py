"""
Setup-Verifikations-Script für VRChat Meeting Moderator Bot
Prüft ob alle Voraussetzungen erfüllt sind.
"""

import sys
import os
import subprocess

def check_python_version():
    """Prüfe Python-Version"""
    print("=" * 50)
    print("1. Python-Version prüfen...")
    print("=" * 50)
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Benötigt Python 3.10+")
        return False

def check_venv():
    """Prüfe ob venv aktiviert ist"""
    print("\n" + "=" * 50)
    print("2. Virtuelle Umgebung prüfen...")
    print("=" * 50)
    
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print(f"✅ Virtuelle Umgebung aktiviert: {sys.prefix}")
        return True
    else:
        print("⚠️  Virtuelle Umgebung nicht aktiviert")
        print("   Aktiviere mit: venv_moderator\\Scripts\\activate.bat (Windows)")
        print("   oder: source venv_moderator/bin/activate (Linux/Mac)")
        return False

def check_dependencies():
    """Prüfe ob alle Dependencies installiert sind"""
    print("\n" + "=" * 50)
    print("3. Dependencies prüfen...")
    print("=" * 50)
    
    required_packages = [
        "aiavatar",
        "openai",
        "httpx",
        "numpy",
        "pyaudio",
        "pyautogui",
        "opencv-python",
        "python-dateutil",
        "pythonosc",
        "resemblyzer"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - FEHLT")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Fehlende Packages: {', '.join(missing)}")
        print("   Installiere mit: pip install -r requirements_all.txt")
        return False
    else:
        print("\n✅ Alle Dependencies installiert")
        return True

def check_environment_variables():
    """Prüfe Umgebungsvariablen"""
    print("\n" + "=" * 50)
    print("4. Umgebungsvariablen prüfen...")
    print("=" * 50)
    
    required_vars = {
        "OPENAI_API_KEY": "Erforderlich - Hole dir einen Key von https://platform.openai.com/api-keys"
    }
    
    optional_vars = {
        "VRChat_INPUT_DEVICE": "Optional - Index von VB-Cable-B Output",
        "VRChat_OUTPUT_DEVICE": "Optional - Index von VB-Cable-A Input",
        "VOICEVOX_URL": "Optional - Standard: http://127.0.0.1:50021",
        "VOICEVOX_SPEAKER": "Optional - Standard: 46",
        "VISION_INTERVAL": "Optional - Standard: 3.0",
        "OSC_HOST": "Optional - Standard: 127.0.0.1",
        "OSC_PORT": "Optional - Standard: 9000"
    }
    
    all_ok = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != "YOUR_OPENAI_API_KEY":
            print(f"✅ {var} = {'*' * 20} (gesetzt)")
        else:
            print(f"❌ {var} - FEHLT")
            print(f"   {description}")
            all_ok = False
    
    print("\nOptionale Variablen:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value}")
        else:
            print(f"⚠️  {var} - Nicht gesetzt ({description})")
    
    return all_ok

def check_audio_devices():
    """Prüfe Audio-Geräte"""
    print("\n" + "=" * 50)
    print("5. Audio-Geräte prüfen...")
    print("=" * 50)
    
    try:
        from aiavatar.device import AudioDevice
        devices = AudioDevice().get_audio_devices()
        
        cable_a_input = None
        cable_b_output = None
        
        print("\nVerfügbare Audio-Geräte:")
        for d in devices:
            name = d["name"]
            if "CABLE-A" in name.upper() and "INPUT" in name.upper():
                cable_a_input = d
                print(f"✅ [{d['index']}] {name} (VB-Cable-A Input)")
            elif "CABLE-B" in name.upper() and "OUTPUT" in name.upper():
                cable_b_output = d
                print(f"✅ [{d['index']}] {name} (VB-Cable-B Output)")
        
        if not cable_a_input:
            print("❌ VB-Cable-A Input nicht gefunden")
            print("   Installiere VB-Cable-A von https://vb-audio.com/Cable/")
        
        if not cable_b_output:
            print("❌ VB-Cable-B Output nicht gefunden")
            print("   Installiere VB-Cable-B von https://vb-audio.com/Cable/")
        
        if cable_a_input and cable_b_output:
            print("\n✅ Beide VB-Cable-Geräte gefunden")
            print(f"   Empfohlene Konfiguration:")
            print(f"   VRChat_INPUT_DEVICE={cable_b_output['index']}")
            print(f"   VRChat_OUTPUT_DEVICE={cable_a_input['index']}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Prüfen der Audio-Geräte: {e}")
        return False

def check_voicevox():
    """Prüfe ob VOICEVOX läuft"""
    print("\n" + "=" * 50)
    print("6. VOICEVOX prüfen (optional)...")
    print("=" * 50)
    
    try:
        import httpx
        voicevox_url = os.getenv("VOICEVOX_URL", "http://127.0.0.1:50021")
        
        response = httpx.get(f"{voicevox_url}/speakers", timeout=2.0)
        if response.status_code == 200:
            print(f"✅ VOICEVOX läuft auf {voicevox_url}")
            return True
        else:
            print(f"⚠️  VOICEVOX antwortet nicht korrekt auf {voicevox_url}")
            return False
    except Exception as e:
        print(f"⚠️  VOICEVOX nicht erreichbar: {e}")
        print("   VOICEVOX ist optional - Bot kann auch ohne laufen")
        return False

def main():
    """Hauptfunktion"""
    print("\n" + "=" * 50)
    print("VRChat Meeting Moderator Bot - Setup-Verifikation")
    print("=" * 50)
    print()
    
    results = {
        "Python": check_python_version(),
        "Virtuelle Umgebung": check_venv(),
        "Dependencies": check_dependencies(),
        "Umgebungsvariablen": check_environment_variables(),
        "Audio-Geräte": check_audio_devices(),
        "VOICEVOX": check_voicevox()
    }
    
    print("\n" + "=" * 50)
    print("Zusammenfassung")
    print("=" * 50)
    
    all_ok = True
    for name, result in results.items():
        status = "✅ OK" if result else "❌ FEHLT"
        print(f"{name}: {status}")
        if not result and name != "VOICEVOX":  # VOICEVOX ist optional
            all_ok = False
    
    print()
    if all_ok:
        print("🎉 Alle Voraussetzungen erfüllt! Du kannst den Bot starten.")
        print("   Starte mit: python vrchat_moderator.py")
    else:
        print("⚠️  Einige Voraussetzungen fehlen noch.")
        print("   Siehe SETUP_ANLEITUNG.md für Details.")
    
    print()

if __name__ == "__main__":
    main()
