from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime  # <-- ADD THIS

class Contact(BaseModel):
    id: Optional[str]
    user_id: str  # To link contact to the user who created it
    first_name: str
    last_name: Optional[str]
    company: Optional[str]
    emails: Optional[List[EmailStr]] = []
    phone_numbers: Optional[List[str]] = []
    address: Optional[str]
    birthday: Optional[str]  # Format: "YYYY-MM-DD"
    username: Optional[str]
    pronouns: Optional[str]
    notes: Optional[str]
    created_at: Optional[datetime] = None  # <-- ADD THIS

class ContactCreate(BaseModel):
    first_name: str
    last_name: Optional[str]
    company: Optional[str]
    emails: Optional[List[EmailStr]] = []
    phone_numbers: Optional[List[str]] = []
    address: Optional[str]
    birthday: Optional[str]
    username: Optional[str]
    pronouns: Optional[str]
    notes: Optional[str]

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    company: Optional[str]
    emails: Optional[List[EmailStr]] = []
    phone_numbers: Optional[List[str]] = []
    address: Optional[str]
    birthday: Optional[str]
    username: Optional[str]
    pronouns: Optional[str]
    notes: Optional[str]
