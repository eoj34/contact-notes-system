from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    username: str
    email: EmailStr
    password: str
    contact_sort_preference: Optional[str] = "alphabetical"  # NEW FIELD

class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    contact_sort_preference: Optional[str] = "alphabetical"  # NEW FIELD
