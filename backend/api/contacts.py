from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

try:
    from backend.database import get_db
    from backend.models.contact import Contact
except ImportError:
    from database import get_db
    from models.contact import Contact

router = APIRouter()


class ContactIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    phone: str = Field(min_length=3, max_length=40)
    relationship: str = ""


@router.get("")
def get_contact(db: Session = Depends(get_db)):
    contact = db.query(Contact).order_by(Contact.id.desc()).first()
    if not contact:
        return None
    return {
        "id": contact.id,
        "name": contact.name,
        "phone": contact.phone,
        "relationship": contact.relationship,
    }


@router.post("")
def set_contact(contact_in: ContactIn, db: Session = Depends(get_db)):
    # Update existing primary or insert new
    existing = db.query(Contact).first()
    if existing:
        existing.name = contact_in.name
        existing.phone = contact_in.phone
        existing.relationship = contact_in.relationship
        contact = existing
    else:
        contact = Contact(
            name=contact_in.name,
            phone=contact_in.phone,
            relationship=contact_in.relationship,
        )
        db.add(contact)
    db.commit()
    db.refresh(contact)
    return {
        "id": contact.id,
        "name": contact.name,
        "phone": contact.phone,
        "relationship": contact.relationship,
    }

