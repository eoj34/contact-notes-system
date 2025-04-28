A simple Contact + Notes Management system, built with FastAPI, MongoDB, and vanilla HTML/JS frontend.
This project supports user signup/login, JWT-based authentication, contact management, note management, and frontend interaction.

Features

JWT Authentication: Secure login/signup flow.
Contact Management: Create, view, edit, and delete your contacts.
Note Management: Attach notes to each contact, with full CRUD functionality.
Field Normalization: Automatically processes incoming note/contact data for consistent backend storage.
RESTful API: Exposes endpoints for users, contacts, and notes.
Frontend: Basic static HTML pages + JavaScript for calling API endpoints.

Tech Stack

FastAPI (Backend Framework)
Motor (Async MongoDB driver)
MongoDB (Database)
HTML/CSS/JavaScript (Frontend)
JWT (Authentication using JSON Web Tokens)
Pydantic (Schema validation)
Uvicorn (ASGI Server)


How to Run Locally:

Clone the Repository:
git clone https://github.com/your-username/contact-notes-system.git
cd contact-notes-system

Set up a Python Virtual Environment:
python3 -m venv venv
source venv/bin/activate   # (or venv\Scripts\activate on Windows)

Install Dependencies:
pip install -r requirements.txt

Ensure MongoDB is Running Locally:
By default, the app connects to:
mongodb://localhost:27017
You must have MongoDB running locally (brew services start mongodb-community on Mac, or through MongoDB Compass)

Run the Application:
source venv/bin/activate   
uvicorn app.main:app --reload

Access the Frontend
Visit http://localhost:8000/static/index.html

Explore API Docs:
FastAPI automatically provides Swagger UI docs at:
http://localhost:8000/docs
