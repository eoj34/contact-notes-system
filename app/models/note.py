from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Note(BaseModel):
    id: Optional[str]
    contact_id: str  
    body: str
    timestamp: datetime

class NoteCreate(BaseModel):
    contact_id: str
    body: str
    timestamp: Optional[datetime] = None

class NoteUpdate(BaseModel):
    body: Optional[str]
