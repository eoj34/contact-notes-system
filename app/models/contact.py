from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime  # <-- Needed for created_at

class Contact(BaseModel):
    id: Optional[str]
    user_id: str  # To link contact to the user who created it
    first_name: str
    last_name: Optional[str] = None
    company: Optional[str] = None
    emails: Optional[List[EmailStr]] = []
    phone_numbers: Optional[List[str]] = []
    address: Optional[str] = None
    birthday: Optional[str] = None  # Format: "YYYY-MM-DD"
    username: Optional[str] = None
    #pronouns: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None  # New field

class ContactCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    company: Optional[str] = None
    emails: Optional[List[EmailStr]] = []
    phone_numbers: Optional[List[str]] = []
    address: Optional[str] = None
    birthday: Optional[str] = None
    username: Optional[str] = None
    #pronouns: Optional[str] = None
    notes: Optional[str] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    emails: Optional[List[EmailStr]] = []
    phone_numbers: Optional[List[str]] = []
    address: Optional[str] = None
    birthday: Optional[str] = None
    username: Optional[str] = None
    #pronouns: Optional[str] = None
    notes: Optional[str] = None

