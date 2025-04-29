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

1. Clone the Repository:
git clone https://github.com/eoj34/contact-notes-system.git
cd contact-notes-system

3. Set up a Python Virtual Environment:
   
macOS:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate

4. Install Dependencies: 
pip install -r requirements.txt

5. Ensure MongoDB is Running Locally:
   
The app connects to:
mongodb://localhost:27017

You must have MongoDB running on your system locally or use your MongoDB cluster by replacing line 4 in database.py

6. Run the Application:
uvicorn app.main:app --reload
(May have to run: source venv/bin/activate before)

7. Access the Frontend:
   
Open this URL in your browser:
http://localhost:8000/static/index.html

8. Explore the API Docs:
FastAPI provides automatic docs:

http://localhost:8000/docs

Key Decisions, Tradeoffs, and Assumptions:

I chose FastAPI as the framework due to its speed, simplicity, and automatic generation of interactive API documentation.
For the database, I selected MongoDB because of its flexibility and ease of handling dynamic schemas, which fits the structure of contacts and notes.

I normalized inbound note data to a standard body field to ensure consistency across all stored notes.
Additionally, I built a simple frontend to allow easier testing directly through a browser, instead of relying solely on Postman.
The frontend allows users to:

Sign up with an email and password
Perform full CRUD operations on contacts and the notes attached to those contacts
Set minor user preferences on their profile page
Tradeoffs:

I did not implement maximum field length validation to keep the system lightweight.
I did not implement user role differentiation; currently, all users have the same access rights.

Assumptions:

The user running the application will have access to a local or cloud MongoDB instance.

What I Would Improve With More Time:

1. I would add Unit and Integration Testing.
2. I would use an event bus for notes.
3. I would add the ability to perform CRUD operations on users without having to manually do It via the database. This would allow users to edit their password/email or delate their account. 
4. I would also build a more detailed frontend. The frontend has a lot of scope for refinement. 
5. I would also add the ability for users to favorite certain contacts. 

