"""
Moderation Tools für VRChat Meeting Moderator

Tools für Meeting-Management, Notizen, Timer, Tracker und Verhaltensanalyse.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


# In-Memory Storage für Meeting-Daten
meeting_data = {
    "notes": [],
    "speakers": {},
    "topics": [],
    "participants": [],
    "behavior_data": {},
    "summaries": []
}


@dataclass
class MeetingNote:
    timestamp: str
    content: str
    speaker: Optional[str] = None
    topic: Optional[str] = None


@dataclass
class SpeakerStats:
    name: str
    total_speaking_time: float
    number_of_turns: int
    last_spoke: Optional[str] = None


@dataclass
class Topic:
    name: str
    started_at: str
    ended_at: Optional[str] = None
    participants: List[str] = None
    notes: List[str] = None


@dataclass
class Participant:
    identifier: str
    first_seen: str
    last_seen: str
    engagement_level: str = "unknown"  # active, passive, distracted
    speaking_time: float = 0.0


@dataclass
class BehaviorAnalysis:
    participant_id: str
    timestamp: str
    engagement_level: str
    activity: str
    visual_signals: List[str] = None


# Meeting Notes Tool
def create_meeting_notes_tool():
    """Tool zum Speichern von Meeting-Notizen"""
    tool_spec = {
        "type": "function",
        "function": {
            "name": "save_meeting_note",
            "description": "Speichere eine Notiz während des Meetings. Nutze dies für wichtige Punkte, Entscheidungen, Action Items oder andere relevante Informationen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Der Inhalt der Notiz"
                    },
                    "speaker": {
                        "type": "string",
                        "description": "Optional: Name oder Identifier des Sprechers"
                    },
                    "topic": {
                        "type": "string",
                        "description": "Optional: Das aktuelle Diskussionsthema"
                    }
                },
                "required": ["content"]
            }
        }
    }
    
    async def save_meeting_note(content: str, speaker: str = None, topic: str = None):
        """Speichere eine Meeting-Notiz"""
        note = MeetingNote(
            timestamp=datetime.now().isoformat(),
            content=content,
            speaker=speaker,
            topic=topic
        )
        meeting_data["notes"].append(asdict(note))
        logger.info(f"Notiz gespeichert: {content[:50]}...")
        return {"status": "saved", "note_id": len(meeting_data["notes"]) - 1}
    
    return tool_spec, save_meeting_note


# Speaker Timer Tool
def create_speaker_timer_tool():
    """Tool zum Tracken der Redezeit pro Sprecher"""
    tool_spec = {
        "type": "function",
        "function": {
            "name": "update_speaker_timer",
            "description": "Aktualisiere die Redezeit-Statistiken für einen Sprecher. Nutze dies wenn ein Sprecher beginnt oder aufhört zu sprechen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "speaker_id": {
                        "type": "string",
                        "description": "Identifier des Sprechers"
                    },
                    "speaking_time_seconds": {
                        "type": "number",
                        "description": "Die Redezeit in Sekunden für diesen Turn"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["start", "end", "update"],
                        "description": "Aktion: 'start' wenn Sprecher beginnt, 'end' wenn aufhört, 'update' für kontinuierliche Updates"
                    }
                },
                "required": ["speaker_id", "action"]
            }
        }
    }
    
    async def update_speaker_timer(speaker_id: str, action: str, speaking_time_seconds: float = 0.0):
        """Aktualisiere Sprecher-Timer"""
        if speaker_id not in meeting_data["speakers"]:
            meeting_data["speakers"][speaker_id] = asdict(SpeakerStats(
                name=speaker_id,
                total_speaking_time=0.0,
                number_of_turns=0
            ))
        
        stats = meeting_data["speakers"][speaker_id]
        
        if action == "start":
            stats["number_of_turns"] = stats.get("number_of_turns", 0) + 1
            stats["last_spoke"] = datetime.now().isoformat()
        elif action == "end" or action == "update":
            stats["total_speaking_time"] = stats.get("total_speaking_time", 0.0) + speaking_time_seconds
        
        meeting_data["speakers"][speaker_id] = stats
        
        return {
            "status": "updated",
            "speaker_id": speaker_id,
            "total_time": stats.get("total_speaking_time", 0.0),
            "turns": stats.get("number_of_turns", 0)
        }
    
    return tool_spec, update_speaker_timer


# Topic Tracker Tool
def create_topic_tracker_tool():
    """Tool zum Verfolgen von Diskussionsthemen"""
    tool_spec = {
        "type": "function",
        "function": {
            "name": "track_topic",
            "description": "Verfolge Diskussionsthemen. Nutze dies wenn ein neues Thema beginnt oder ein Thema abgeschlossen wird.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic_name": {
                        "type": "string",
                        "description": "Name des Themas"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["start", "end"],
                        "description": "'start' wenn Thema beginnt, 'end' wenn abgeschlossen"
                    },
                    "participants": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: Liste der Teilnehmer die an diesem Thema teilnehmen"
                    }
                },
                "required": ["topic_name", "action"]
            }
        }
    }
    
    async def track_topic(topic_name: str, action: str, participants: List[str] = None):
        """Verfolge ein Diskussionsthema"""
        if action == "start":
            topic = Topic(
                name=topic_name,
                started_at=datetime.now().isoformat(),
                participants=participants or [],
                notes=[]
            )
            meeting_data["topics"].append(asdict(topic))
            return {"status": "started", "topic": topic_name}
        elif action == "end":
            # Finde das letzte Thema mit diesem Namen
            for topic in reversed(meeting_data["topics"]):
                if topic["name"] == topic_name and topic.get("ended_at") is None:
                    topic["ended_at"] = datetime.now().isoformat()
                    return {"status": "ended", "topic": topic_name}
            return {"status": "not_found", "topic": topic_name}
    
    return tool_spec, track_topic


# Participant Tracker Tool
def create_participant_tracker_tool():
    """Tool zum Verwalten der Teilnehmer-Liste"""
    tool_spec = {
        "type": "function",
        "function": {
            "name": "update_participant",
            "description": "Aktualisiere Teilnehmer-Informationen. Nutze dies wenn ein neuer Teilnehmer erkannt wird oder sich Teilnehmer-Status ändert.",
            "parameters": {
                "type": "object",
                "properties": {
                    "participant_id": {
                        "type": "string",
                        "description": "Identifier des Teilnehmers"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["add", "update", "remove"],
                        "description": "Aktion: 'add' für neuen Teilnehmer, 'update' für Status-Update, 'remove' wenn Teilnehmer geht"
                    },
                    "engagement_level": {
                        "type": "string",
                        "enum": ["active", "passive", "distracted", "unknown"],
                        "description": "Engagement-Level des Teilnehmers"
                    }
                },
                "required": ["participant_id", "action"]
            }
        }
    }
    
    async def update_participant(participant_id: str, action: str, engagement_level: str = "unknown"):
        """Aktualisiere Teilnehmer-Informationen"""
        now = datetime.now().isoformat()
        
        if action == "add":
            participant = Participant(
                identifier=participant_id,
                first_seen=now,
                last_seen=now,
                engagement_level=engagement_level
            )
            meeting_data["participants"].append(asdict(participant))
            return {"status": "added", "participant_id": participant_id}
        
        elif action == "update":
            for p in meeting_data["participants"]:
                if p["identifier"] == participant_id:
                    p["last_seen"] = now
                    if engagement_level != "unknown":
                        p["engagement_level"] = engagement_level
                    return {"status": "updated", "participant_id": participant_id}
            return {"status": "not_found", "participant_id": participant_id}
        
        elif action == "remove":
            meeting_data["participants"] = [
                p for p in meeting_data["participants"] 
                if p["identifier"] != participant_id
            ]
            return {"status": "removed", "participant_id": participant_id}
    
    return tool_spec, update_participant


# Behavior Analyzer Tool
def create_behavior_analyzer_tool():
    """Tool für Verhaltensanalyse der Teilnehmer"""
    tool_spec = {
        "type": "function",
        "function": {
            "name": "analyze_behavior",
            "description": "Analysiere das Verhalten eines Teilnehmers. Nutze dies für Engagement-Level, Aktivitäten und visuelle Signale.",
            "parameters": {
                "type": "object",
                "properties": {
                    "participant_id": {
                        "type": "string",
                        "description": "Identifier des Teilnehmers"
                    },
                    "engagement_level": {
                        "type": "string",
                        "enum": ["active", "passive", "distracted", "interested", "disengaged"],
                        "description": "Engagement-Level basierend auf visueller Beobachtung"
                    },
                    "activity": {
                        "type": "string",
                        "description": "Beschreibung der aktuellen Aktivität (z.B. 'speaking', 'listening', 'raising_hand', 'leaving')"
                    },
                    "visual_signals": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: Liste von visuellen Signalen (z.B. 'hand_raised', 'nodding', 'looking_away')"
                    }
                },
                "required": ["participant_id", "engagement_level", "activity"]
            }
        }
    }
    
    async def analyze_behavior(
        participant_id: str,
        engagement_level: str,
        activity: str,
        visual_signals: List[str] = None
    ):
        """Analysiere Teilnehmer-Verhalten"""
        analysis = BehaviorAnalysis(
            participant_id=participant_id,
            timestamp=datetime.now().isoformat(),
            engagement_level=engagement_level,
            activity=activity,
            visual_signals=visual_signals or []
        )
        
        if participant_id not in meeting_data["behavior_data"]:
            meeting_data["behavior_data"][participant_id] = []
        
        meeting_data["behavior_data"][participant_id].append(asdict(analysis))
        
        return {
            "status": "analyzed",
            "participant_id": participant_id,
            "engagement_level": engagement_level,
            "activity": activity
        }
    
    return tool_spec, analyze_behavior


# Visual Context Tool
def create_visual_context_tool():
    """Tool zum Abfragen der aktuellen visuellen Situation"""
    tool_spec = {
        "type": "function",
        "function": {
            "name": "get_visual_context",
            "description": "Frage die aktuelle visuelle Situation im Meeting ab. Nutze dies um zu sehen wer anwesend ist, was gerade passiert und aktuelle Aktivitäten.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "enum": ["participants", "activities", "current_situation", "all"],
                        "description": "Was abgefragt werden soll: 'participants' für Teilnehmer-Liste, 'activities' für aktuelle Aktivitäten, 'current_situation' für Gesamt-Überblick, 'all' für alles"
                    }
                },
                "required": ["query"]
            }
        }
    }
    
    async def get_visual_context(query: str):
        """Hole visuellen Kontext"""
        result = {}
        
        if query == "participants" or query == "all":
            result["participants"] = meeting_data["participants"]
        
        if query == "activities" or query == "all":
            # Aktuelle Aktivitäten aus behavior_data
            current_activities = {}
            for participant_id, behaviors in meeting_data["behavior_data"].items():
                if behaviors:
                    latest = behaviors[-1]
                    current_activities[participant_id] = {
                        "engagement": latest.get("engagement_level"),
                        "activity": latest.get("activity"),
                        "visual_signals": latest.get("visual_signals", [])
                    }
            result["activities"] = current_activities
        
        if query == "current_situation" or query == "all":
            result["current_situation"] = {
                "total_participants": len(meeting_data["participants"]),
                "active_topics": len([t for t in meeting_data["topics"] if t.get("ended_at") is None]),
                "total_notes": len(meeting_data["notes"]),
                "timestamp": datetime.now().isoformat()
            }
        
        return result
    
    return tool_spec, get_visual_context


# Summary Generator Tool
def create_summary_generator_tool():
    """Tool zum Generieren von Zusammenfassungen"""
    tool_spec = {
        "type": "function",
        "function": {
            "name": "generate_summary",
            "description": "Generiere eine Zusammenfassung des Meetings oder eines bestimmten Zeitraums. Nutze dies für regelmäßige Updates oder Meeting-Abschluss.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary_type": {
                        "type": "string",
                        "enum": ["full", "recent", "topics", "decisions"],
                        "description": "Art der Zusammenfassung: 'full' für vollständig, 'recent' für letzte Aktivitäten, 'topics' für Themen-Überblick, 'decisions' für Entscheidungen"
                    },
                    "include_participants": {
                        "type": "boolean",
                        "description": "Soll Teilnehmer-Liste eingeschlossen werden?"
                    }
                },
                "required": ["summary_type"]
            }
        }
    }
    
    async def generate_summary(summary_type: str, include_participants: bool = True):
        """Generiere Zusammenfassung"""
        summary = {
            "type": summary_type,
            "timestamp": datetime.now().isoformat(),
            "content": {}
        }
        
        if summary_type == "full" or summary_type == "recent":
            # Notizen
            if summary_type == "recent":
                # Letzte 10 Notizen
                notes = meeting_data["notes"][-10:]
            else:
                notes = meeting_data["notes"]
            
            summary["content"]["notes"] = [n["content"] for n in notes]
        
        if summary_type == "full" or summary_type == "topics":
            # Themen
            summary["content"]["topics"] = [
                {
                    "name": t["name"],
                    "started": t["started_at"],
                    "ended": t.get("ended_at")
                }
                for t in meeting_data["topics"]
            ]
        
        if summary_type == "full" or summary_type == "decisions":
            # Entscheidungen (aus Notizen extrahieren)
            decisions = [
                n["content"] for n in meeting_data["notes"]
                if "entscheidung" in n["content"].lower() or "decision" in n["content"].lower()
            ]
            summary["content"]["decisions"] = decisions
        
        if include_participants:
            summary["content"]["participants"] = [
                {
                    "id": p["identifier"],
                    "engagement": p.get("engagement_level")
                }
                for p in meeting_data["participants"]
            ]
        
        # Speichere Zusammenfassung
        meeting_data["summaries"].append(summary)
        
        return summary
    
    return tool_spec, generate_summary


def get_all_tools():
    """Hole alle Moderation-Tools"""
    tools = [
        create_meeting_notes_tool(),
        create_speaker_timer_tool(),
        create_topic_tracker_tool(),
        create_participant_tracker_tool(),
        create_behavior_analyzer_tool(),
        create_visual_context_tool(),
        create_summary_generator_tool(),
    ]
    return tools


def get_meeting_data():
    """Hole alle Meeting-Daten (für Export/Backup)"""
    return meeting_data


def reset_meeting_data():
    """Setze Meeting-Daten zurück (für neues Meeting)"""
    global meeting_data
    meeting_data = {
        "notes": [],
        "speakers": {},
        "topics": [],
        "participants": [],
        "behavior_data": {},
        "summaries": []
    }
