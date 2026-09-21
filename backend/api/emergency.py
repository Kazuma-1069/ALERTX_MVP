from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

try:
    from backend.database import get_db
    from backend.models.emergency import Emergency
except ImportError:
    from database import get_db
    from models.emergency import Emergency

router = APIRouter()


class LocationIn(BaseModel):
    latitude: float
    longitude: float
    accuracy: float | None = None


@router.post("/start")
def start_emergency(db: Session = Depends(get_db)):
    session_id = f"AX-{uuid4().hex[:6].upper()}"
    emergency = Emergency(
        session_id=session_id,
        status="active",
        created_at=datetime.now(timezone.utc),
    )
    db.add(emergency)
    db.commit()
    db.refresh(emergency)
    return {
        "session_id": emergency.session_id,
        "status": emergency.status,
        "created_at": emergency.created_at.isoformat() if emergency.created_at else None,
    }


@router.post("/{session_id}/location")
def update_location(session_id: str, location: LocationIn, db: Session = Depends(get_db)):
    emergency = db.query(Emergency).filter(Emergency.session_id == session_id).first()
    if not emergency:
        return {"error": "session_not_found"}
    emergency.latitude = location.latitude
    emergency.longitude = location.longitude
    emergency.accuracy = location.accuracy
    db.commit()
    db.refresh(emergency)
    return {
        "session_id": emergency.session_id,
        "status": emergency.status,
        "latitude": emergency.latitude,
        "longitude": emergency.longitude,
        "accuracy": emergency.accuracy,
    }


@router.get("/{session_id}")
def get_emergency(session_id: str, db: Session = Depends(get_db)):
    emergency = db.query(Emergency).filter(Emergency.session_id == session_id).first()
    if not emergency:
        return {"error": "session_not_found"}
    return {
        "session_id": emergency.session_id,
        "status": emergency.status,
        "latitude": emergency.latitude,
        "longitude": emergency.longitude,
        "accuracy": emergency.accuracy,
        "created_at": emergency.created_at.isoformat() if emergency.created_at else None,
        "completed_at": emergency.completed_at.isoformat() if emergency.completed_at else None,
    }


@router.post("/{session_id}/complete")
def complete_emergency(session_id: str, db: Session = Depends(get_db)):
    emergency = db.query(Emergency).filter(Emergency.session_id == session_id).first()
    if not emergency:
        return {"error": "session_not_found"}
    emergency.status = "completed"
    emergency.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(emergency)
    return {
        "session_id": emergency.session_id,
        "status": emergency.status,
        "completed_at": emergency.completed_at.isoformat() if emergency.completed_at else None,
    }

