This is a Contact + Notes Management system, built with FastAPI, MongoDB, and vanilla HTML/JS frontend.
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

How to Run This Project Locally: 

1. Clone the Repository
git clone https://github.com/eoj34/contact-notes-system.git
cd contact-notes-system

3. Set up a Python Virtual Environment
   
macOS:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Ensure MongoDB is Running Locally
   
The app connects to:
mongodb://localhost:27017

You must have MongoDB running on your system locally or use your MongoDB cluster by replacing line 4 in database.py

6. Run the Application:
uvicorn app.main:app --reload
(May have to run: source venv/bin/activate before)

7. Access the Frontend
   
Open this URL in your browser:
http://localhost:8000/static/index.html

8. Explore the API Docs
FastAPI provides automatic docs:

http://localhost:8000/docs
