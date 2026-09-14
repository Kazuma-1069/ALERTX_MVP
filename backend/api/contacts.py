from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()
_memory = None

class ContactIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    phone: str = Field(min_length=3, max_length=40)
    relationship: str = ""

@router.get("")
def get_contact():
    return _memory

@router.post("")
def set_contact(contact: ContactIn):
    global _memory
    _memory = contact.model_dump()
    return _memory
