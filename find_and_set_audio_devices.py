"""
Script zum Finden und Setzen der Audio-Geräte-Indizes
Führt automatisch die Geräte-Erkennung durch und zeigt die Konfiguration
"""

import os
import sys

# Füge aktuelles Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from aiavatar.device import AudioDevice
    
    print("=" * 60)
    print("VB-CABLE Geräte-Suche")
    print("=" * 60)
    print()
    
    audio_device = AudioDevice()
    devices = audio_device.get_audio_devices()
    
    cable_output = None  # Bot hört VRChat (Input-Device für Bot)
    cable_input = None   # Bot spricht zu VRChat (Output-Device für Bot)
    
    print("Suche nach CABLE-Geräten...")
    print()
    
    for d in devices:
        name_upper = d["name"].upper()
        if "CABLE" in name_upper:
            print(f"Gefunden: [{d['index']}] {d['name']}")
            print(f"  Input-Kanäle: {d['max_input_channels']}, Output-Kanäle: {d['max_output_channels']}")
            
            # CABLE Output = Bot hört VRChat (Input-Device)
            if "OUTPUT" in name_upper and d["max_input_channels"] > 0:
                cable_output = d
                print(f"  [OK] Als Input-Device erkannt (Bot hoert VRChat)")
            
            # CABLE Input = Bot spricht zu VRChat (Output-Device)
            if "INPUT" in name_upper and d["max_output_channels"] > 0:
                cable_input = d
                print(f"  [OK] Als Output-Device erkannt (Bot spricht zu VRChat)")
            print()
    
    print("=" * 60)
    print("Ergebnis")
    print("=" * 60)
    print()
    
    if cable_output and cable_input:
        print("[OK] Beide VB-CABLE Geraete gefunden!")
        print()
        print("Konfiguration:")
        print(f"  VRChat_INPUT_DEVICE={cable_output['index']}  # {cable_output['name']}")
        print(f"  VRChat_OUTPUT_DEVICE={cable_input['index']}  # {cable_input['name']}")
        print()
        print("Diese Werte werden automatisch vom Bot verwendet.")
        print("Du kannst sie auch in .env Datei setzen:")
        print()
        print(f"VRChat_INPUT_DEVICE={cable_output['index']}")
        print(f"VRChat_OUTPUT_DEVICE={cable_input['index']}")
    elif cable_output or cable_input:
        print("[WARNUNG] Nur ein VB-CABLE Geraet gefunden!")
        if cable_output:
            print(f"  Gefunden: [{cable_output['index']}] {cable_output['name']} (Input)")
        if cable_input:
            print(f"  Gefunden: [{cable_input['index']}] {cable_input['name']} (Output)")
        print()
        print("Bitte installiere beide VB-CABLE Geräte (A und B)")
    else:
        print("[FEHLER] Keine VB-CABLE Geraete gefunden!")
        print()
        print("Bitte installiere VB-CABLE von: https://vb-audio.com/Cable/")
        print("Du brauchst beide Geräte: VB-Cable-A und VB-Cable-B")
    
    print()
    
except ImportError as e:
    print("FEHLER: Konnte AIAvatarKit nicht importieren.")
    print("Stelle sicher, dass:")
    print("  1. Die virtuelle Umgebung aktiviert ist")
    print("  2. Alle Dependencies installiert sind: pip install -e .")
    print()
    print(f"Fehler: {e}")
    sys.exit(1)
except Exception as e:
    print(f"FEHLER: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
