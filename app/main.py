from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth_routes, contact_routes, note_routes
from app.routes import user_routes


app = FastAPI()

# Include your API routes
app.include_router(auth_routes.router)
app.include_router(contact_routes.router)
app.include_router(note_routes.router)
app.include_router(user_routes.router)
# Serve static frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact Notes System!"}
