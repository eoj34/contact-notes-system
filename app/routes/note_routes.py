from fastapi import APIRouter, Depends, Header, HTTPException
from app.models.note import Note, NoteCreate, NoteUpdate
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
async def create_note(note: NoteCreate, user_id: str = Depends(get_current_user)):
    note_data = note.dict()
    note_data = normalize_note_fields(note_data)
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

# --- NEW DELETE endpoint ---
@router.delete("/{note_id}")
async def delete_note(note_id: str, user_id: str = Depends(get_current_user)):
    result = await notes_collection.delete_one({"_id": ObjectId(note_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found or not authorized to delete")
    return {"message": "Note deleted successfully"}

# --- NEW UPDATE endpoint ---
@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, updated_fields: NoteUpdate, user_id: str = Depends(get_current_user)):
    update_data = {k: v for k, v in updated_fields.dict().items() if v is not None}  # only send non-None fields
    update_data = normalize_note_fields(update_data)
    update_data["timestamp"] = datetime.utcnow()

    result = await notes_collection.find_one_and_update(
        {"_id": ObjectId(note_id), "user_id": user_id},
        {"$set": update_data},
        return_document=True
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Note not found or not authorized to update")
    
    result["id"] = str(result["_id"])
    return Note(**result)

@router.get("/{note_id}", response_model=Note)
async def get_single_note(note_id: str, user_id: str = Depends(get_current_user)):
    note = await notes_collection.find_one({"_id": ObjectId(note_id), "user_id": user_id})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note["id"] = str(note["_id"])
    return Note(**note)
