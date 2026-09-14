from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()
_sessions = {}

class LocationIn(BaseModel):
    latitude: float
    longitude: float
    accuracy: float | None = None

@router.post("/start")
def start_emergency():
    session_id = f"AX-{uuid4().hex[:6].upper()}"
    _sessions[session_id] = {
        "session_id": session_id,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    return _sessions[session_id]

@router.post("/{session_id}/location")
def update_location(session_id: str, location: LocationIn):
    if session_id not in _sessions:
        return {"error": "session_not_found"}
    _sessions[session_id].update({
        "latitude": location.latitude,
        "longitude": location.longitude,
        "accuracy": location.accuracy
    })
    return _sessions[session_id]

@router.get("/{session_id}")
def get_emergency(session_id: str):
    return _sessions.get(session_id, {"error": "session_not_found"})

@router.post("/{session_id}/complete")
def complete_emergency(session_id: str):
    if session_id not in _sessions:
        return {"error": "session_not_found"}
    _sessions[session_id]["status"] = "completed"
    _sessions[session_id]["completed_at"] = datetime.now(timezone.utc).isoformat()
    return _sessions[session_id]
