"""
VRChat Meeting Moderator Bot

Ein AI-Moderator-Bot für VRChat-Meetings mit kontinuierlicher visueller Beobachtung
und Echtzeit-Verhaltensanalyse der Teilnehmer.
"""

import asyncio
import base64
import io
import logging
import os
import pyautogui
from typing import Optional, Dict, Any
from datetime import datetime
from dateutil.parser import parse as parse_datetime

# Lade .env Datei (MUSS VOR allen anderen Imports sein!)
try:
    from dotenv import load_dotenv
    # Lade .env aus dem Projektverzeichnis
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"✓ .env Datei geladen: {env_path}")
    else:
        print(f"⚠️ .env Datei nicht gefunden: {env_path}")
except ImportError:
    print("⚠️ python-dotenv nicht installiert. Installiere mit: pip install python-dotenv")
except Exception as e:
    print(f"⚠️ Fehler beim Laden der .env Datei: {e}")

from aiavatar import AIAvatar
from aiavatar.face.vrchat import VRChatFaceController
from aiavatar.animation.vrchat import VRChatAnimationController
from aiavatar.sts.stt.speaker_gate import MainSpeakerGate
from aiavatar.device import AudioDevice
from aiavatar.sts.llm import Tool
from aiavatar.sts.models import STSRequest

# Import Moderation Tools
from moderation_tools import (
    get_all_tools,
    reset_meeting_data
)

# OpenAI TTS für professionelle englische/deutsche Stimmen
from aiavatar.sts.tts.openai import OpenAISpeechSynthesizer

# Konfiguration (wird aus .env geladen, wenn vorhanden)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# OpenAI TTS Konfiguration (statt VOICEVOX)
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "tts-1-hd")  # "tts-1" für schnell, "tts-1-hd" für Qualität
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")  # Optionen: alloy, echo, fable, onyx, nova, shimmer

# Initialisiere Audio-Geräte (wird in main() aufgerufen)
VRChat_INPUT_DEVICE = -1
VRChat_OUTPUT_DEVICE = -1

# Vision-Konfiguration
VISION_INTERVAL = float(os.getenv("VISION_INTERVAL", "3.0"))  # Sekunden zwischen Screenshots
VRChat_WINDOW_REGION = os.getenv("VRChat_WINDOW_REGION", None)  # Optional: (x, y, width, height)

# OSC-Konfiguration für VRChat
OSC_HOST = os.getenv("OSC_HOST", "127.0.0.1")
OSC_PORT = int(os.getenv("OSC_PORT", "9000"))

# Face Controller Konfiguration (OPTIONAL)
# Setze auf "false" oder "0" um Face Controller zu deaktivieren (Bot funktioniert auch ohne)
ENABLE_FACE_CONTROLLER = os.getenv("ENABLE_FACE_CONTROLLER", "true").lower() in ("true", "1", "yes")

logger = logging.getLogger(__name__)


def setup_logging(debug: bool = False):
    """Konfiguriere Logging"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def find_cable_devices():
    """Finde automatisch VB-CABLE Geräte und setze die Indizes"""
    try:
        audio_device = AudioDevice()
        devices = audio_device.get_audio_devices()
        
        cable_output = None  # Bot hört VRChat (Input-Device für Bot)
        cable_input = None   # Bot spricht zu VRChat (Output-Device für Bot)
        
        for d in devices:
            name_upper = d["name"].upper()
            # CABLE Output = Bot hört VRChat (Input-Device)
            if "CABLE" in name_upper and "OUTPUT" in name_upper and d["max_input_channels"] > 0:
                cable_output = d
            # CABLE Input = Bot spricht zu VRChat (Output-Device)
            if "CABLE" in name_upper and "INPUT" in name_upper and d["max_output_channels"] > 0:
                cable_input = d
        
        return cable_output, cable_input
    except Exception as e:
        logger.warning(f"Konnte Audio-Geräte nicht automatisch finden: {e}")
        return None, None


def get_vrchat_audio_devices():
    """Ermittle VRChat Audio-Geräte automatisch oder aus Umgebungsvariablen"""
    # Prüfe zuerst Umgebungsvariablen
    input_device = os.getenv("VRChat_INPUT_DEVICE")
    output_device = os.getenv("VRChat_OUTPUT_DEVICE")
    
    if input_device and output_device:
        # Beide sind gesetzt, verwende diese
        return int(input_device), int(output_device)
    
    # Versuche automatische Erkennung
    try:
        cable_output, cable_input = find_cable_devices()
        
        if cable_output and cable_input:
            logger.info(f"VB-CABLE Geräte automatisch gefunden:")
            logger.info(f"  Input-Device (Bot hört VRChat): [{cable_output['index']}] {cable_output['name']}")
            logger.info(f"  Output-Device (Bot spricht zu VRChat): [{cable_input['index']}] {cable_input['name']}")
            return cable_output['index'], cable_input['index']
        elif cable_output or cable_input:
            logger.warning("Nur ein VB-CABLE Gerät gefunden. Bitte beide installieren.")
    except Exception as e:
        logger.debug(f"Automatische Geräte-Erkennung fehlgeschlagen: {e}")
    
    # Fallback zu Umgebungsvariablen oder -1
    input_idx = int(input_device) if input_device else -1
    output_idx = int(output_device) if output_device else -1
    
    return input_idx, output_idx


def list_audio_devices():
    """Liste verfügbare Audio-Geräte auf"""
    print("=== Verfügbare Audio-Geräte ===")
    audio_device = AudioDevice()
    devices = audio_device.get_audio_devices()
    
    print("\nInput-Geräte (Mikrofone):")
    for d in devices:
        if d["max_input_channels"] > 0:
            marker = " <-- CABLE Output (Bot hört VRChat)" if "CABLE" in d["name"].upper() and "OUTPUT" in d["name"].upper() else ""
            print(f"  [{d['index']}] {d['name']}{marker}")
    
    print("\nOutput-Geräte (Lautsprecher):")
    for d in devices:
        if d["max_output_channels"] > 0:
            marker = " <-- CABLE Input (Bot spricht zu VRChat)" if "CABLE" in d["name"].upper() and "INPUT" in d["name"].upper() else ""
            print(f"  [{d['index']}] {d['name']}{marker}")
    
    return devices


def create_vrchat_face_controller() -> VRChatFaceController:
    """Erstelle VRChatFaceController mit professionellen Ausdrücken"""
    faces = {
        "neutral": 0,      # Immer neutral auf 0 setzen
        "attentive": 1,   # Aufmerksam
        "friendly": 2,    # Freundlich
        "thinking": 3,    # Nachdenklich
        "speaking": 4,    # Sprechend
        "listening": 5,   # Zuhörend
    }
    
    return VRChatFaceController(
        osc_address="/avatar/parameters/FaceOSC",
        faces=faces,
        neutral_key="neutral",
        host=OSC_HOST,
        port=OSC_PORT,
        debug=True
    )


def create_openai_tts(openai_api_key: str) -> OpenAISpeechSynthesizer:
    """Erstelle OpenAI TTS Synthesizer für professionelle englische/deutsche Stimmen"""
    return OpenAISpeechSynthesizer(
        openai_api_key=openai_api_key,
        model=OPENAI_TTS_MODEL,  # Konfigurierbar über Umgebungsvariable
        speaker=OPENAI_TTS_VOICE,  # Konfigurierbar über Umgebungsvariable
        audio_format="wav",
        debug=True
    )


def create_vrchat_animation_controller() -> VRChatAnimationController:
    """Erstelle VRChatAnimationController mit Moderations-Gesten"""
    animations = {
        "idling": 0,
        "attention": 1,   # Aufmerksamkeit erregen
        "quiet": 2,       # Ruhe signalisieren
        "pointing": 3,    # Zeigen
        "welcoming": 4,   # Begrüßung
    }
    
    return VRChatAnimationController(
        osc_address="/avatar/parameters/VRCEmote",
        animations=animations,
        idling_key="idling",
        host=OSC_HOST,
        port=OSC_PORT,
        debug=True
    )


def create_moderation_system_prompt() -> str:
    """Erstelle System Prompt für Meeting-Moderation"""
    return """Du bist ein professioneller Meeting-Moderator für VRChat-Meetings mit kontinuierlicher visueller Beobachtung.

## Deine Vision-Fähigkeiten

Du siehst kontinuierlich, was im Meeting passiert:
- Automatische Screenshots alle 2-5 Sekunden zeigen dir die aktuelle Situation
- Du kannst das Verhalten der Teilnehmer analysieren: Körpersprache, Bewegungen, Aktivitäten
- Du erkennst wer spricht, wer reagiert, wer passiv ist
- Du beobachtest Engagement-Level und Gruppendynamik
- Du reagierst auf visuelle Signale (z.B. jemand hebt Hand, jemand verlässt Raum)

## Moderations-Regeln

1. **Sprecher-Erkennung und -Verwaltung**:
   - Nutze Audio UND Video für Sprecher-Erkennung
   - Erkenne Sprecher-Wechsel basierend auf Audio und visuellen Signalen
   - Stelle sicher, dass alle Teilnehmer die Chance haben zu sprechen

2. **Themenführung**:
   - Führe die Diskussion strukturiert
   - Berücksichtige visuelle Reaktionen der Teilnehmer
   - Erkenne wenn ein Thema abgeschlossen ist oder ein neues beginnt

3. **Zeitmanagement**:
   - Überwache die Redezeit pro Sprecher
   - Erkenne Engagement-Level: Wer ist aktiv, wer ist passiv
   - Stelle sicher, dass das Meeting effizient bleibt

4. **Zusammenfassungen**:
   - Erstelle regelmäßig Zusammenfassungen der Diskussion
   - Berücksichtige visuelle Beobachtungen in deinen Zusammenfassungen
   - Dokumentiere wichtige Entscheidungen und Action Items

## Face Expressions

Du hast folgende Gesichtsausdrücke:
- neutral: Standard-Ausdruck
- attentive: Aufmerksam und konzentriert
- friendly: Freundlich und einladend
- thinking: Nachdenklich, während du überlegst
- speaking: Während du sprichst
- listening: Während du zuhörst

Nutze [face:attentive] wenn du die Aufmerksamkeit der Teilnehmer brauchst.
Nutze [face:friendly] für Begrüßungen und positive Rückmeldungen.

## Automatische Vision-Updates

Du erhältst automatisch visuelle Updates über die aktuelle Situation im Meeting.
Du musst nicht explizit nach Screenshots fragen - sie werden dir automatisch bereitgestellt.
Nutze diese Informationen für eine bessere Moderation.

## Beispiel-Verhalten

- Wenn jemand die Hand hebt (visuell erkennbar): "Ich sehe, dass jemand die Hand hebt. Bitte, Sie haben das Wort."
- Wenn jemand den Raum verlässt: "Ich bemerke, dass jemand den Raum verlassen hat."
- Wenn die Diskussion ins Stocken gerät: "Ich sehe, dass die Diskussion pausiert. Sollten wir zum nächsten Thema übergehen?"
- Bei visuellen Reaktionen: "Ich sehe positive Reaktionen zu diesem Vorschlag."

Sei professionell, freundlich und hilfreich. Nutze deine visuellen Fähigkeiten für eine bessere Moderation."""


# Globale Variablen für Vision-System
vision_task: Optional[asyncio.Task] = None
last_screenshot: Optional[bytes] = None
visual_context: Dict[str, Any] = {}
last_visual_update_time: float = 0.0
VISUAL_UPDATE_INTERVAL = 10.0  # Sekunden zwischen visuellen Kontext-Updates

# Globale Variablen für Echo-Unterdrückung
bot_speaking: bool = False
last_bot_speech_time: float = 0.0
ECHO_SUPPRESSION_DURATION = 2.0  # Sekunden nach Bot-Sprache, in denen Audio ignoriert wird


async def capture_vrchat_screenshot() -> Optional[bytes]:
    """Erfasse Screenshot vom VRChat-Fenster"""
    try:
        if VRChat_WINDOW_REGION:
            # Wenn Region spezifiziert, verwende diese
            import ast
            region = ast.literal_eval(VRChat_WINDOW_REGION)
            screenshot = pyautogui.screenshot(region=region)
        else:
            # Vollbild-Screenshot
            screenshot = pyautogui.screenshot()
        
        # Konvertiere zu Bytes
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        return buffered.getvalue()
    except Exception as e:
        logger.error(f"Fehler beim Screenshot: {e}")
        return None


def image_to_base64(image_bytes: bytes) -> str:
    """Konvertiere Bild-Bytes zu Base64-URL"""
    b64_encoded = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/png;base64,{b64_encoded}"


async def analyze_meeting_scene(image_bytes: bytes, aiavatar_app: AIAvatar = None) -> Dict[str, Any]:
    """Analysiere Meeting-Szene mit LLM-Vision"""
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "image_size": len(image_bytes),
        "analyzed": False
    }
    
    # Wenn LLM verfügbar, nutze Vision für detaillierte Analyse
    if aiavatar_app and aiavatar_app.sts and aiavatar_app.sts.llm:
        try:
            # Konvertiere Bild zu Base64
            image_url = image_to_base64(image_bytes)
            
            # Erstelle Vision-Request für LLM-Analyse
            # Dies wird als automatischer Kontext-Update gesendet
            analysis["image_url"] = image_url
            analysis["analyzed"] = True
            
            # Die eigentliche LLM-Analyse wird in update_visual_context durchgeführt
        except Exception as e:
            logger.error(f"Fehler bei Bildanalyse: {e}")
    
    return analysis


def get_context_schema_from_llm_service(llm_service) -> str:
    """Ermittle das richtige context_schema basierend auf dem LLM-Service"""
    service_name = llm_service.__class__.__name__.lower()
    
    if "chatgpt" in service_name or "openai" in service_name:
        return "chatgpt"
    elif "claude" in service_name:
        return "claude"
    elif "gemini" in service_name:
        return "gemini"
    else:
        # Default zu chatgpt Format
        return "chatgpt"


async def update_visual_context(
    aiavatar_app: AIAvatar,
    session_id: str,
    image_bytes: bytes,
    analysis: Dict[str, Any]
):
    """Aktualisiere visuellen Kontext automatisch im LLM"""
    global last_visual_update_time
    
    try:
        import time
        current_time = time.time()
        
        # Rate-Limiting: Nur alle VISUAL_UPDATE_INTERVAL Sekunden aktualisieren
        if current_time - last_visual_update_time < VISUAL_UPDATE_INTERVAL:
            return
        
        # Erstelle automatischen Kontext-Update mit Bild
        image_url = image_to_base64(image_bytes)
        
        # Sende visuellen Update als Kontext-Historie
        # Nutze context_manager um automatische Updates hinzuzufügen
        if aiavatar_app.sts and aiavatar_app.sts.llm and aiavatar_app.sts.llm.context_manager:
            # Nutze die aktuelle session_id als context_id
            context_id = session_id
            llm_service = aiavatar_app.sts.llm
            
            # Ermittle das richtige context_schema
            context_schema = get_context_schema_from_llm_service(llm_service)
            
            # Erstelle visuelle Update-Nachricht
            visual_update_text = f"""$[Visual Update: {analysis.get('timestamp')}]

Aktuelle visuelle Situation im Meeting wurde aktualisiert. 
Analysiere das Bild für Teilnehmer-Erkennung, Verhalten und Aktivitäten.
Beobachte: Wer ist anwesend, wer spricht, wer zeigt Reaktionen, Engagement-Level, visuelle Signale."""
            
            # Format abhängig vom LLM-Service
            if context_schema == "chatgpt":
                # Format für ChatGPT/OpenAI
                visual_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": visual_update_text
                        }
                    ]
                }
            elif context_schema == "claude":
                # Format für Claude
                visual_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": image_url
                            }
                        },
                        {
                            "type": "text",
                            "text": visual_update_text
                        }
                    ]
                }
            elif context_schema == "gemini":
                # Format für Gemini (wird in compose_messages verarbeitet)
                visual_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": visual_update_text
                        }
                    ]
                }
            else:
                # Fallback zu chatgpt Format
                visual_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": visual_update_text
                        }
                    ]
                }
            
            # Füge zum Kontext hinzu
            await llm_service.context_manager.add_histories(
                context_id=context_id,
                data_list=[visual_message],
                context_schema=context_schema
            )
            
            last_visual_update_time = current_time
            logger.debug(f"Visueller Kontext aktualisiert: {analysis.get('timestamp')} (Schema: {context_schema})")
        
    except Exception as e:
        logger.error(f"Fehler beim Update des visuellen Kontexts: {e}")


def detect_significant_changes(new_analysis: Dict[str, Any], old_analysis: Dict[str, Any]) -> bool:
    """Erkenne signifikante Änderungen für Delta-Detection"""
    # Einfache Implementierung: Immer als signifikant betrachten
    # Später kann dies erweitert werden mit Bildvergleich oder LLM-basierter Änderungserkennung
    if not old_analysis:
        return True
    
    # Prüfe auf Zeit-Unterschied (z.B. mehr als 5 Sekunden)
    if "timestamp" in new_analysis and "timestamp" in old_analysis:
        try:
            new_time = parse_datetime(new_analysis["timestamp"])
            old_time = parse_datetime(old_analysis["timestamp"])
            time_diff = (new_time - old_time).total_seconds()
            
            # Wenn mehr als 5 Sekunden vergangen, als signifikant betrachten
            if time_diff > 5.0:
                return True
        except Exception:
            # Bei Parse-Fehler: als signifikant betrachten
            return True
    
    return True  # Für jetzt: Immer aktualisieren


async def continuous_vision_worker(aiavatar_app: AIAvatar, session_id: str):
    """Kontinuierliche Vision-Überwachung: Screenshots und Analyse"""
    global last_screenshot, visual_context
    
    logger.info("Kontinuierliche Vision-Überwachung gestartet")
    old_analysis = {}
    
    while True:
        try:
            await asyncio.sleep(VISION_INTERVAL)
            
            # Screenshot aufnehmen
            screenshot_bytes = await capture_vrchat_screenshot()
            if not screenshot_bytes:
                continue
            
            # Analysiere Szene
            analysis = await analyze_meeting_scene(screenshot_bytes, aiavatar_app)
            
            # Delta-Detection: Nur bei signifikanten Änderungen
            if detect_significant_changes(analysis, old_analysis):
                visual_context.update(analysis)
                last_screenshot = screenshot_bytes
                
                # Automatische Kontext-Updates an LLM senden
                await update_visual_context(aiavatar_app, session_id, screenshot_bytes, analysis)
                
                old_analysis = analysis.copy()
                logger.debug(f"Vision-Update: {analysis.get('timestamp')}")
            
        except asyncio.CancelledError:
            logger.info("Vision-Überwachung beendet")
            break
        except Exception as e:
            logger.error(f"Fehler in Vision-Worker: {e}")
            await asyncio.sleep(1)


def setup_speaker_diarization(aiavatar_app: AIAvatar):
    """Richte Speaker Diarization für mehrere Sprecher ein"""
    global bot_speaking, last_bot_speech_time, ECHO_SUPPRESSION_DURATION
    
    speaker_gate = MainSpeakerGate(
        accept_threshold=0.55,
        pair_lock_threshold=0.72
    )
    
    # STT Preprocessing: Sprecher-Erkennung und Echo-Unterdrückung
    @aiavatar_app.sts.stt.preprocess
    async def stt_preprocess(session_id: str, audio_bytes: bytes):
        global bot_speaking, last_bot_speech_time
        import time
        
        current_time = time.time()
        
        # Wenn Bot gerade spricht oder kürzlich gesprochen hat, ignoriere Audio (Echo-Unterdrückung)
        if bot_speaking or (current_time - last_bot_speech_time) < ECHO_SUPPRESSION_DURATION:
            logger.debug("Ignoriere Audio während/nach Bot-Sprache (Echo-Unterdrückung)")
            return None, {"ignored": True, "reason": "echo_suppression"}
        
        # Für Meetings: Alle Sprecher akzeptieren, aber annotieren sie
        gate_response = await speaker_gate.evaluate(
            session_id, 
            audio_bytes, 
            aiavatar_app.sts.vad.sample_rate
        )
        
        # In Meetings akzeptieren wir alle Sprecher, aber annotieren sie
        return audio_bytes, {
            "speaker_gate": gate_response.to_dict(),
            "speaker_confidence": gate_response.confidence,
            "main_speaker_locked": gate_response.main_locked
        }
    
    # STT Postprocessing: Sprecher-Informationen zum Kontext hinzufügen
    @aiavatar_app.sts.stt.postprocess
    async def stt_postprocess(
        session_id: str, 
        text: str, 
        audio_bytes: bytes, 
        preprocess_metadata: dict
    ):
        speaker_info = preprocess_metadata.get("speaker_gate", {})
        confidence = speaker_info.get("confidence")
        main_locked = speaker_info.get("main_locked", False)
        
        # Füge Sprecher-Informationen zum Text hinzu
        if confidence is not None:
            speaker_note = f"$[Speaker: confidence={confidence:.2f}, main_locked={main_locked}]"
            annotated_text = f"{speaker_note}\n\n{text}"
            return annotated_text, preprocess_metadata
        
        return text, preprocess_metadata


async def main():
    """Hauptfunktion"""
    setup_logging(debug=True)
    
    # Audio-Geräte automatisch finden oder aus Umgebungsvariablen lesen
    global VRChat_INPUT_DEVICE, VRChat_OUTPUT_DEVICE
    VRChat_INPUT_DEVICE, VRChat_OUTPUT_DEVICE = get_vrchat_audio_devices()
    
    # Audio-Geräte auflisten (für Konfiguration)
    if VRChat_INPUT_DEVICE < 0 or VRChat_OUTPUT_DEVICE < 0:
        print("\n=== WICHTIG: Audio-Geräte konfigurieren ===")
        list_audio_devices()
        print("\nVB-CABLE Geräte konnten nicht automatisch gefunden werden.")
        print("Bitte setze VRChat_INPUT_DEVICE und VRChat_OUTPUT_DEVICE Umgebungsvariablen")
        print("oder passe sie in vrchat_moderator.py an.\n")
        print("Beispiel:")
        print("  set VRChat_INPUT_DEVICE=6   # Index von CABLE Output")
        print("  set VRChat_OUTPUT_DEVICE=13 # Index von CABLE Input")
        return
    
    # VRChat Controller erstellen
    # Face Controller ist OPTIONAL - Bot funktioniert auch ohne FaceOSC
    face_controller = None
    if ENABLE_FACE_CONTROLLER:
        try:
            face_controller = create_vrchat_face_controller()
            logger.info("Face Controller aktiviert (FaceOSC wird verwendet)")
        except Exception as e:
            logger.warning(f"Face Controller konnte nicht initialisiert werden: {e}")
            logger.info("Bot läuft ohne Face Controller (keine Gesichtsausdrücke)")
            face_controller = None
    else:
        logger.info("Face Controller deaktiviert (Bot läuft ohne Gesichtsausdrücke)")
    
    animation_controller = create_vrchat_animation_controller()
    
    # System Prompt erstellen
    system_prompt = create_moderation_system_prompt()
    
    # OpenAI TTS erstellen (für professionelle englische/deutsche Stimmen)
    tts = create_openai_tts(OPENAI_API_KEY)
    
    # AIAvatar erstellen
    aiavatar_app = AIAvatar(
        openai_api_key=OPENAI_API_KEY,
        system_prompt=system_prompt,
        tts=tts,  # Verwende OpenAI TTS statt VOICEVOX
        input_device_index=VRChat_INPUT_DEVICE,
        output_device_index=VRChat_OUTPUT_DEVICE,
        face_controller=face_controller,
        animation_controller=animation_controller,
        debug=True
    )
    
    # Speaker Diarization einrichten
    setup_speaker_diarization(aiavatar_app)
    
    # Moderation Tools hinzufügen
    logger.info("Registriere Moderation Tools...")
    tools = get_all_tools()
    for tool_spec, tool_func in tools:
        tool = Tool(
            name=tool_spec["function"]["name"],
            spec=tool_spec,
            func=tool_func
        )
        aiavatar_app.sts.llm.add_tool(tool)
        logger.debug(f"Tool registriert: {tool.name}")
    
    # Vision-System: get_image_url Funktion
    @aiavatar_app.get_image_url
    async def get_image_url(source: str) -> str:
        """Bereitstellung von Screenshots für LLM"""
        if source == "screenshot" or source == "camera":
            screenshot_bytes = await capture_vrchat_screenshot()
            if screenshot_bytes:
                return image_to_base64(screenshot_bytes)
        return ""
    
    # Response Callbacks für Echo-Unterdrückung
    @aiavatar_app.on_response("start")
    async def on_start_response(response):
        """Callback wenn Response startet"""
        global bot_speaking, last_bot_speech_time
        import time
        bot_speaking = True  # Markiere dass Bot spricht
        last_bot_speech_time = time.time()  # Zeitpunkt speichern
        if aiavatar_app.face_controller:
            await aiavatar_app.face_controller.set_face("listening", 3.0)
    
    @aiavatar_app.on_response("chunk")
    async def on_chunk_response(response):
        """Callback für Response-Chunks"""
        global last_bot_speech_time
        import time
        if aiavatar_app.face_controller and response.metadata.get("is_first_chunk"):
            await aiavatar_app.face_controller.set_face("speaking", 0.0)  # Dauer 0 = bis Reset
        # Aktualisiere Zeitpunkt (Bot spricht noch)
        last_bot_speech_time = time.time()
    
    @aiavatar_app.on_response("final")
    async def on_final_response(response):
        """Callback wenn Response beendet ist"""
        global bot_speaking, last_bot_speech_time
        import time
        bot_speaking = False  # Bot spricht nicht mehr
        last_bot_speech_time = time.time()  # Zeitpunkt für Echo-Unterdrückung
    
    # Meeting-Daten zurücksetzen für neues Meeting
    reset_meeting_data()
    
    # Kontinuierliche Vision-Überwachung starten
    global vision_task
    session_id = "vrchat_moderator_session"
    vision_task = asyncio.create_task(
        continuous_vision_worker(aiavatar_app, session_id)
    )
    
    # Prüfe API Key BEVOR Bot gestartet wird
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY" or not OPENAI_API_KEY or len(OPENAI_API_KEY) < 10:
        logger.error("=" * 60)
        logger.error("❌ FEHLER: OPENAI_API_KEY nicht gesetzt!")
        logger.error("=" * 60)
        logger.error("Bitte setze OPENAI_API_KEY in .env Datei oder als Umgebungsvariable.")
        logger.error("")
        logger.error("Option 1: Erstelle .env Datei im Projektverzeichnis:")
        logger.error("  OPENAI_API_KEY=sk-dein-api-key-hier")
        logger.error("")
        logger.error("Option 2: Setze Umgebungsvariable:")
        logger.error('  $env:OPENAI_API_KEY="sk-dein-api-key-hier"')
        logger.error("")
        logger.error("Siehe auch: ENV_SETUP_ANLEITUNG.md")
        logger.error("=" * 60)
        return
    
    logger.info("VRChat Meeting Moderator Bot gestartet")
    logger.info("Warte auf Meeting-Teilnehmer...")
    
    # Debug: Prüfe Konfiguration
    logger.info(f"✓ API Key gesetzt: {OPENAI_API_KEY[:10]}...{OPENAI_API_KEY[-4:]}")
    logger.info(f"✓ Input Device: {VRChat_INPUT_DEVICE}, Output Device: {VRChat_OUTPUT_DEVICE}")
    
    try:
        # Bot starten (blockiert bis beendet)
        logger.info("Starte Bot-Listening (blockiert bis beendet)...")
        
        # Prüfe Audio-Geräte vor Start
        try:
            logger.info("Prüfe Audio-Geräte...")
            if hasattr(aiavatar_app, 'audio_recorder'):
                logger.info(f"Audio Recorder: Device Index {aiavatar_app.audio_recorder.device_index}, Sample Rate {aiavatar_app.audio_recorder.sample_rate}")
                # Versuche Audio-Stream zu testen
                try:
                    import pyaudio
                    p = pyaudio.PyAudio()
                    device_info = p.get_device_info_by_index(aiavatar_app.audio_recorder.device_index)
                    logger.info(f"Audio Input Device Info: {device_info.get('name')}, Max Input Channels: {device_info.get('maxInputChannels')}")
                    if device_info.get('maxInputChannels', 0) == 0:
                        logger.error("❌ FEHLER: Audio-Gerät hat keine Input-Kanäle! Das Gerät kann nicht für Audio-Input verwendet werden.")
                    else:
                        # Versuche Stream zu öffnen
                        try:
                            test_stream = p.open(
                                rate=aiavatar_app.audio_recorder.sample_rate,
                                channels=aiavatar_app.audio_recorder.channels,
                                format=pyaudio.paInt16,
                                input=True,
                                frames_per_buffer=aiavatar_app.audio_recorder.chunk_size,
                                input_device_index=aiavatar_app.audio_recorder.device_index
                            )
                            logger.info("✓ Audio-Stream kann geöffnet werden")
                            test_stream.stop_stream()
                            test_stream.close()
                        except OSError as stream_error:
                            error_code = getattr(stream_error, 'errno', None)
                            if error_code == -9999:
                                logger.warning("⚠️ Audio-Gerät kann momentan nicht geöffnet werden (möglicherweise von VRChat verwendet)")
                                logger.warning("Der Bot wird automatisch versuchen, das Gerät zu öffnen, wenn es verfügbar ist.")
                            else:
                                logger.error(f"❌ FEHLER: Audio-Stream kann nicht geöffnet werden: {stream_error}", exc_info=True)
                        except Exception as stream_error:
                            logger.error(f"❌ FEHLER: Audio-Stream kann nicht geöffnet werden: {stream_error}", exc_info=True)
                    p.terminate()
                except Exception as audio_test_error:
                    logger.error(f"❌ FEHLER beim Testen des Audio-Geräts: {audio_test_error}", exc_info=True)
            if hasattr(aiavatar_app, 'audio_player'):
                logger.info(f"Audio Player: Device Index {aiavatar_app.audio_player.device_index}")
        except Exception as e:
            logger.warning(f"Fehler beim Prüfen der Audio-Geräte: {e}")
        
        # Wrapper für start_listening mit erweitertem Debugging
        async def start_listening_with_debug():
            """Wrapper für start_listening mit erweitertem Debugging"""
            logger.info("Initialisiere Session...")
            try:
                await aiavatar_app.initialize_session(session_id, "moderator", None)
                logger.info("✓ Session initialisiert")
            except Exception as e:
                logger.error(f"❌ Fehler bei Session-Initialisierung: {e}", exc_info=True)
                raise
            
            logger.info("Starte send_microphone_task...")
            try:
                # Wrapper für send_microphone_worker mit Error-Handling und Retry-Logik
                async def send_microphone_worker_with_error_handling(session_id: str):
                    """Wrapper für send_microphone_worker mit Error-Handling und Retry"""
                    max_retries = 5
                    retry_delay = 2.0  # Sekunden
                    
                    for attempt in range(max_retries):
                        try:
                            logger.info(f"Öffne Audio-Stream... (Versuch {attempt + 1}/{max_retries})")
                            stream_gen = aiavatar_app.audio_recorder.start_stream()
                            logger.info("✓ Audio-Stream-Generator erstellt, starte Loop...")
                            
                            async for data in stream_gen:
                                if not aiavatar_app.cancel_echo or not aiavatar_app.audio_player.is_playing:
                                    await aiavatar_app.send_microphone_data(data, session_id)
                            
                            # Wenn wir hier ankommen, wurde der Stream normal beendet
                            logger.info("Audio-Stream wurde normal beendet")
                            break
                            
                        except OSError as stream_error:
                            error_code = getattr(stream_error, 'errno', None)
                            if error_code == -9999:  # Unanticipated host error
                                if attempt < max_retries - 1:
                                    logger.warning(f"⚠️ Audio-Gerät kann nicht geöffnet werden (Versuch {attempt + 1}/{max_retries})")
                                    logger.warning("Mögliche Ursachen:")
                                    logger.warning("  - VRChat verwendet das Gerät bereits")
                                    logger.warning("  - Anderes Programm blockiert das Gerät")
                                    logger.warning(f"  - Warte {retry_delay} Sekunden und versuche es erneut...")
                                    await asyncio.sleep(retry_delay)
                                    retry_delay *= 1.5  # Exponentielles Backoff
                                else:
                                    logger.error(f"❌ FEHLER: Audio-Gerät kann nach {max_retries} Versuchen nicht geöffnet werden!")
                                    logger.error("Bitte stelle sicher, dass:")
                                    logger.error("  1. VRChat das Audio-Gerät nicht verwendet")
                                    logger.error("  2. Kein anderes Programm das Gerät blockiert")
                                    logger.error("  3. Das Gerät in den Windows-Audio-Einstellungen verfügbar ist")
                                    raise
                            else:
                                logger.error(f"❌ FEHLER im Audio-Stream: {stream_error}", exc_info=True)
                                raise
                        except Exception as stream_error:
                            logger.error(f"❌ FEHLER im Audio-Stream: {stream_error}", exc_info=True)
                            logger.error("Audio-Stream wurde beendet. Bot kann nicht weiterlaufen.")
                            raise
                
                aiavatar_app.send_microphone_task = asyncio.create_task(
                    send_microphone_worker_with_error_handling(session_id)
                )
                logger.info("✓ send_microphone_task erstellt")
            except Exception as e:
                logger.error(f"❌ Fehler beim Erstellen von send_microphone_task: {e}", exc_info=True)
                raise
            
            logger.info("Starte receive_response_task...")
            try:
                aiavatar_app.receive_response_task = asyncio.create_task(
                    aiavatar_app.receive_response_worker()
                )
                logger.info("✓ receive_response_task erstellt")
            except Exception as e:
                logger.error(f"❌ Fehler beim Erstellen von receive_response_task: {e}", exc_info=True)
                raise
            
            # Warte kurz und prüfe Tasks
            await asyncio.sleep(0.2)
            
            if aiavatar_app.send_microphone_task.done():
                logger.error("❌ send_microphone_task wurde sofort beendet!")
                try:
                    await aiavatar_app.send_microphone_task
                except Exception as e:
                    logger.error(f"❌ Fehler in send_microphone_task: {e}", exc_info=True)
                    raise
            else:
                logger.info("✓ send_microphone_task läuft")
            
            if aiavatar_app.receive_response_task.done():
                logger.error("❌ receive_response_task wurde sofort beendet!")
                try:
                    await aiavatar_app.receive_response_task
                except Exception as e:
                    logger.error(f"❌ Fehler in receive_response_task: {e}", exc_info=True)
                    raise
            else:
                logger.info("✓ receive_response_task läuft")
            
            # Warte auf beide Tasks mit kontinuierlichem Monitoring
            logger.info("Warte auf Tasks (Bot läuft jetzt)...")
            
            async def monitor_tasks_continuously():
                """Überwache Tasks kontinuierlich und logge Status"""
                while True:
                    await asyncio.sleep(1.0)  # Prüfe alle Sekunde
                    
                    if aiavatar_app.send_microphone_task.done():
                        logger.error("❌ send_microphone_task wurde beendet!")
                        try:
                            await aiavatar_app.send_microphone_task
                        except Exception as e:
                            logger.error(f"❌ Fehler in send_microphone_task: {e}", exc_info=True)
                        break
                    
                    if aiavatar_app.receive_response_task.done():
                        logger.error("❌ receive_response_task wurde beendet!")
                        try:
                            await aiavatar_app.receive_response_task
                        except Exception as e:
                            logger.error(f"❌ Fehler in receive_response_task: {e}", exc_info=True)
                        break
                    
                    logger.debug("✓ Beide Tasks laufen noch...")
            
            # Starte Monitoring parallel
            monitor_task = asyncio.create_task(monitor_tasks_continuously())
            
            try:
                results = await asyncio.gather(
                    aiavatar_app.send_microphone_task,
                    aiavatar_app.receive_response_task,
                    return_exceptions=True
                )
                
                # Stoppe Monitoring
                monitor_task.cancel()
                try:
                    await monitor_task
                except asyncio.CancelledError:
                    pass
                
                # Prüfe Ergebnisse auf Fehler
                if isinstance(results[0], Exception):
                    logger.error(f"❌ Fehler in send_microphone_task: {results[0]}", exc_info=True)
                    raise results[0]
                if isinstance(results[1], Exception):
                    logger.error(f"❌ Fehler in receive_response_task: {results[1]}", exc_info=True)
                    raise results[1]
                
                logger.info("✓ Beide Tasks wurden normal beendet")
                    
            except Exception as e:
                logger.error(f"❌ Fehler in asyncio.gather: {e}", exc_info=True)
                monitor_task.cancel()
                raise
        
        # Starte Bot mit erweitertem Debugging
        try:
            await start_listening_with_debug()
            logger.info("Bot-Listening beendet")
        except Exception as start_error:
            logger.error(f"❌ Fehler beim Starten des Bots: {start_error}", exc_info=True)
            
            # Prüfe Tasks auf Fehler
            if hasattr(aiavatar_app, 'send_microphone_task') and aiavatar_app.send_microphone_task:
                if aiavatar_app.send_microphone_task.done():
                    try:
                        await aiavatar_app.send_microphone_task
                    except Exception as task_e:
                        logger.error(f"❌ Fehler in send_microphone_task: {task_e}", exc_info=True)
            
            if hasattr(aiavatar_app, 'receive_response_task') and aiavatar_app.receive_response_task:
                if aiavatar_app.receive_response_task.done():
                    try:
                        await aiavatar_app.receive_response_task
                    except Exception as task_e:
                        logger.error(f"❌ Fehler in receive_response_task: {task_e}", exc_info=True)
            
            raise
    except KeyboardInterrupt:
        logger.info("Bot wird beendet (KeyboardInterrupt)...")
    except Exception as e:
        logger.error(f"Fehler beim Starten des Bots: {e}", exc_info=True)
        # Prüfe Tasks auf Fehler
        if hasattr(aiavatar_app, 'send_microphone_task') and aiavatar_app.send_microphone_task:
            if aiavatar_app.send_microphone_task.done():
                try:
                    await aiavatar_app.send_microphone_task
                except Exception as task_e:
                    logger.error(f"Fehler in send_microphone_task: {task_e}", exc_info=True)
        if hasattr(aiavatar_app, 'receive_response_task') and aiavatar_app.receive_response_task:
            if aiavatar_app.receive_response_task.done():
                try:
                    await aiavatar_app.receive_response_task
                except Exception as task_e:
                    logger.error(f"Fehler in receive_response_task: {task_e}", exc_info=True)
        raise
    finally:
        # Vision-Task beenden
        logger.info("Beende Vision-Task...")
        if vision_task:
            vision_task.cancel()
            try:
                await vision_task
            except asyncio.CancelledError:
                pass


if __name__ == "__main__":
    asyncio.run(main())
