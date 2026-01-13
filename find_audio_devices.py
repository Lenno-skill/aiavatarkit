"""Temporäres Script zum Finden der Audio-Geräte-Indizes"""
import pyaudio

p = pyaudio.PyAudio()

print("=== Alle Audio-Geräte ===")
cable_devices = []

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    name = info.get('name', '')
    
    if 'CABLE' in name.upper():
        cable_devices.append({
            'index': i,
            'name': name,
            'max_input_channels': info.get('maxInputChannels', 0),
            'max_output_channels': info.get('maxOutputChannels', 0)
        })
        print(f"Index {i}: {name}")
        print(f"  Input-Kanäle: {info.get('maxInputChannels', 0)}, Output-Kanäle: {info.get('maxOutputChannels', 0)}")
        print()

p.terminate()

# Finde die richtigen Geräte
cable_output = None  # Bot hört VRChat (Input-Device für Bot)
cable_input = None   # Bot spricht zu VRChat (Output-Device für Bot)

for d in cable_devices:
    name_upper = d['name'].upper()
    # CABLE Output = Bot hört VRChat (Input-Device)
    if 'OUTPUT' in name_upper and d['max_input_channels'] > 0:
        cable_output = d
    # CABLE Input = Bot spricht zu VRChat (Output-Device)
    if 'INPUT' in name_upper and d['max_output_channels'] > 0:
        cable_input = d

print("\n=== Empfohlene Konfiguration ===")
if cable_output:
    print(f"VRChat_INPUT_DEVICE={cable_output['index']}  # {cable_output['name']} (Bot hört VRChat)")
else:
    print("⚠️  CABLE Output nicht gefunden!")

if cable_input:
    print(f"VRChat_OUTPUT_DEVICE={cable_input['index']}  # {cable_input['name']} (Bot spricht zu VRChat)")
else:
    print("⚠️  CABLE Input nicht gefunden!")
