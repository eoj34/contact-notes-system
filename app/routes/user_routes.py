from fastapi import APIRouter, Depends, Header, HTTPException
from app.database import db
from app.auth.jwt_handler import decode_access_token
from app.utils.normalization import normalize_user_fields
from bson import ObjectId

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

users_collection = db.users

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        user_id = payload["sub"]
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/profile")
async def get_profile(user_id: str = Depends(get_current_user)):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "email": user.get("email"),
        "username": user.get("username"),
        "contact_sort_preference": user.get("contact_sort_preference", "alphabetical")
    }

@router.put("/profile")
async def update_profile_sort_preference(data: dict, user_id: str = Depends(get_current_user)):
    sort_preference = data.get("contact_sort_preference")
    if sort_preference not in ["alphabetical", "date_created"]:
        raise HTTPException(status_code=400, detail="Invalid sort preference")

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"contact_sort_preference": sort_preference}}
    )
    return {"message": "Preference updated"}

# (Optional) If you have a signup route, normalize user input there
@router.post("/signup")
async def signup(user_data: dict):
    user_data = normalize_user_fields(user_data)
    # continue saving user_data into users_collection
