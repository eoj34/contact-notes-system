from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Note(BaseModel):
    id: Optional[str]
    contact_id: str  
    title: str        
    body: str
    timestamp: datetime

class NoteCreate(BaseModel):
    contact_id: str
    title: str        
    body: str
    timestamp: Optional[datetime] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None   
    body: Optional[str] = None
