from fastapi import APIRouter, Depends, Header, HTTPException
from app.models.note import Note, NoteCreate
from app.database import db
from app.auth.jwt_handler import decode_access_token
from app.utils.normalization import normalize_note_fields
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

notes_collection = db.notes

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        user_id = payload["sub"]
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=Note)
async def create_note(note: dict, user_id: str = Depends(get_current_user)):
    note_data = normalize_note_fields(note)  # <-- Normalize note fields
    note_data["user_id"] = user_id
    note_data["timestamp"] = datetime.utcnow()
    result = await notes_collection.insert_one(note_data)
    note_data["id"] = str(result.inserted_id)
    return Note(**note_data)

@router.get("/contact/{contact_id}", response_model=list[Note])
async def get_notes_for_contact(contact_id: str, user_id: str = Depends(get_current_user)):
    notes_cursor = notes_collection.find({"contact_id": contact_id, "user_id": user_id}).sort("timestamp", -1)

    notes = []
    async for note in notes_cursor:
        note["id"] = str(note["_id"])
        notes.append(Note(**note))
    return notes
