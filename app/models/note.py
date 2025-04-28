from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Note(BaseModel):
    id: Optional[str]
    contact_id: str  
    title: str        # <-- ADD this
    body: str
    timestamp: datetime

class NoteCreate(BaseModel):
    contact_id: str
    title: str        # <-- ADD this
    body: str
    timestamp: Optional[datetime] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None   # <-- ADD this
    body: Optional[str] = None
