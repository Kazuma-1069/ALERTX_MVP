from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
try:
    from backend.database import Base
except ImportError:
    from database import Base

class Emergency(Base):
    __tablename__ = "emergencies"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(40), unique=True, nullable=False)
    status = Column(String(30), default="active")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
