from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.contact import Contact, ContactCreate, ContactUpdate
from app.database import db
from app.auth.jwt_handler import decode_access_token
from app.utils.normalization import normalize_contact_fields
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)

contacts_collection = db.contacts

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        user_id = payload["sub"]
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

@router.post("/", response_model=Contact)
async def create_contact(contact: ContactCreate, user_id: str = Depends(get_current_user)):
    contact_data = contact.dict()
    contact_data = normalize_contact_fields(contact_data)
    contact_data["user_id"] = user_id
    contact_data["created_at"] = datetime.utcnow()

    print("About to insert contact:", contact_data)  # <-- ADD THIS

    result = await contacts_collection.insert_one(contact_data)

    print("Insert result:", result.inserted_id)  # <-- ADD THIS

    contact_data["id"] = str(result.inserted_id)
    return Contact(**contact_data)


@router.get("/", response_model=list[Contact])
async def get_contacts(user_id: str = Depends(get_current_user)):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    sort_preference = user.get("contact_sort_preference", "alphabetical")

    if sort_preference == "alphabetical":
        contacts_cursor = contacts_collection.find({"user_id": user_id}).sort("first_name", 1)
    else:
        contacts_cursor = contacts_collection.find({"user_id": user_id}).sort("created_at", -1)

    contacts = []
    async for contact in contacts_cursor:
        contact["id"] = str(contact["_id"])
        contacts.append(Contact(**contact))
    return contacts

@router.get("/{contact_id}", response_model=Contact)
async def get_contact(contact_id: str, user_id: str = Depends(get_current_user)):
    contact = await contacts_collection.find_one({"_id": ObjectId(contact_id), "user_id": user_id})
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact["id"] = str(contact["_id"])
    return Contact(**contact)

@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: str, contact_update: ContactUpdate, user_id: str = Depends(get_current_user)):
    update_data = {k: v for k, v in contact_update.dict().items() if v is not None}
    update_data = normalize_contact_fields(update_data)  # <-- Normalize update data
    result = await contacts_collection.find_one_and_update(
        {"_id": ObjectId(contact_id), "user_id": user_id},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    result["id"] = str(result["_id"])
    return Contact(**result)

@router.delete("/{contact_id}")
async def delete_contact(contact_id: str, user_id: str = Depends(get_current_user)):
    result = await contacts_collection.delete_one({"_id": ObjectId(contact_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}
