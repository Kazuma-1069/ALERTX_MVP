from sqlalchemy import Column, Integer, String
try:
    from backend.database import Base
except ImportError:
    from database import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(40), nullable=False)
    relationship = Column(String(50), default="")
