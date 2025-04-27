from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserIn, UserOut
from app.database import db
from app.auth.jwt_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_collection = db.users

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/signup", response_model=UserOut)
async def signup(user: UserIn):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_pw
    result = await users_collection.insert_one(user_dict)

    return UserOut(id=str(result.inserted_id), username=user.username, email=user.email)

@router.post("/login")
async def login(user: UserIn):
    existing_user = await users_collection.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(existing_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}
