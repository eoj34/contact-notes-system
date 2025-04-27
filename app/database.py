from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)
db = client["contact_notes_db"]
