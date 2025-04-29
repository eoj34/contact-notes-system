const API_URL = "http://localhost:8000";

// ------------------- SIGNUP -------------------
async function signup(email, password) {
    const response = await fetch(`${API_URL}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: email,
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (response.status === 200) {
        document.getElementById("signupMessage").innerText = "Account created! You can now login.";
    } else {
        document.getElementById("signupMessage").innerText = "Error";
    }
}

// ------------------- LOGIN -------------------
async function login(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: email,
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/static/contacts.html";
    } else {
        document.getElementById("message").innerText = "Login failed.";
    }
}

// ------------------- LOAD CONTACTS -------------------
async function loadContacts() {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_URL}/contacts/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const contacts = await response.json();
    const contactList = document.getElementById("contactList");
    contactList.innerHTML = "";

    contacts.forEach(contact => {
        const li = document.createElement("li");
        li.innerText = `${contact.first_name} ${contact.last_name}`;
        li.style.cursor = "pointer";

        li.addEventListener("click", () => {
            localStorage.setItem("selected_contact_id", contact.id);
            window.location.href = "/static/contact_detail.html";
        });

        contactList.appendChild(li);
    });
}


// ------------------- CREATE NEW CONTACT -------------------
async function createContact(
    first_name, last_name, company, emails, phone_numbers,
    address, birthday, username, notes
) {
    const token = localStorage.getItem("token");

    await fetch(`${API_URL}/contacts/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            first_name: first_name || "",
            last_name: last_name || "",
            company: company || "",
            emails: emails ? emails.split(",").map(e => e.trim()).filter(e => e) : [],
            phone_numbers: phone_numbers ? phone_numbers.split(",").map(p => p.trim()).filter(p => p) : [],
            address: address || "",
            birthday: birthday || "",
            username: username || "",
            notes: notes || ""
        })
    });
}

// ------------------- LOAD NOTES -------------------
async function loadNotes() {
    const token = localStorage.getItem("token");
    const contactId = localStorage.getItem("selected_contact_id");

    const response = await fetch(`${API_URL}/notes/contact/${contactId}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const notes = await response.json();
    const noteList = document.getElementById("noteList");
    noteList.innerHTML = "";

    notes.forEach(note => {
        const li = document.createElement("li");
        li.innerHTML = `
            <a href="#" onclick="goToNoteDetail('${note.id}')">
                ${new Date(note.timestamp).toLocaleString()} - ${note.body.substring(0, 30)}...
            </a>
        `;
        noteList.appendChild(li);
    });
}

function goToNoteDetail(noteId) {
    localStorage.setItem("selected_note_id", noteId);
    window.location.href = "/static/note_detail.html";
}

async function loadNoteDetail() {
    const token = localStorage.getItem("token");
    const noteId = localStorage.getItem("selected_note_id");

    const response = await fetch(`${API_URL}/notes/${noteId}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.ok) {
        const note = await response.json();

        console.log("Loaded note:", note);  // DEBUGGING
        console.log("note.title is:", note.title);
        console.log("note.body is:", note.body);
        console.log("document.getElementById('note_title'):", document.getElementById("note_title"));
        console.log("document.getElementById('note_body'):", document.getElementById("note_body"));

        const titleInput = document.getElementById("note_title");
        const bodyTextarea = document.getElementById("note_body");

        if (titleInput && bodyTextarea) {
            titleInput.value = note.title || "(No Title)";
            bodyTextarea.value = note.body || "(No Body)";
        } else {
            console.error("Title input or body textarea not found in DOM!");
        }

        window.currentNoteId = note.id;
    } else {
        alert("Failed to load note details.");
    }
}

async function loadContactName(contactId) {
    const token = localStorage.getItem('token');
    const response = await fetch(`http://localhost:8000/contacts/${contactId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        const contact = await response.json();
        const contactName = contact.first_name || "Contact";
        document.getElementById("contactNameHeader").innerText = `Notes for ${contactName}`;
    } else {
        console.error("Failed to load contact info");
    }
}


// ------------------- CREATE NEW NOTE -------------------
async function createNote() {
    const token = localStorage.getItem("token");
    const contactId = localStorage.getItem("selected_contact_id");
    
    const noteTitle = document.getElementById("note_title").value.trim();
    const noteBody = document.getElementById("note_body").value.trim();

    if (!contactId) {
        alert("No contact selected! Cannot create note.");
        return;
    }

    if (!noteTitle || !noteBody) {
        alert("Please provide both a title and a body for the note.");
        return;
    }

    const response = await fetch(`${API_URL}/notes/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            contact_id: contactId,
            title: noteTitle,
            body: noteBody,
            timestamp: null
        })
    });

    if (response.ok) {
        alert("Note created!");
        loadNotes();
    } else {
        const errorData = await response.json();  
        console.error("Error creating note:", errorData);
        alert("Failed to create note.");
    }
}



async function updateNote(noteId) {
    const token = localStorage.getItem("token");
    const newBody = document.getElementById("note_body").value;

    const response = await fetch(`${API_URL}/notes/${noteId}`, {
        method: "PUT",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ body: newBody })
    });

    if (response.ok) {
        alert("Note updated successfully!");
        window.location.href = "/static/notes.html";
    } else {
        alert("Failed to update note.");
    }
}

function enableNoteEditing() {
    const titleInput = document.getElementById("note_title");
    const bodyTextarea = document.getElementById("note_body");
    if (titleInput && bodyTextarea) {
        titleInput.disabled = false;
        bodyTextarea.disabled = false;
    }
}

async function saveNoteChanges() {
    const noteId = window.currentNoteId;
    if (!noteId) {
        alert("No note selected.");
        return;
    }

    const token = localStorage.getItem("token");
    const title = document.getElementById("note_title").value.trim();
    const body = document.getElementById("note_body").value.trim();

    if (!title || !body) {
        alert("Title and body cannot be empty!");
        return;
    }

    const response = await fetch(`${API_URL}/notes/${noteId}`, {
        method: "PUT",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title: title, body: body })
    });

    if (response.ok) {
        alert("Note updated successfully!");
        window.location.reload();
    } else {
        alert("Failed to update note.");
    }
}

async function deleteCurrentNote() {
    const noteId = window.currentNoteId;
    if (!noteId) {
        alert("No note selected.");
        return;
    }

    if (!confirm("Are you sure you want to delete this note?")) {
        return;
    }

    const token = localStorage.getItem("token");

    const response = await fetch(`${API_URL}/notes/${noteId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.ok) {
        alert("Note deleted successfully!");
        window.location.href = "/static/notes.html";
    } else {
        alert("Failed to delete note.");
    }
}



// ------------------- LOAD PROFILE -------------------
async function loadProfile() {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_URL}/users/profile`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const profile = await response.json();

    const profileDiv = document.getElementById("profileInfo");
    if (profileDiv) {
        profileDiv.innerHTML = `
            <p><strong>Email:</strong> ${profile.email}</p>

            <h2>Contact Sort Preference</h2>
            <select id="contactSortPreference">
                <option value="alphabetical">Alphabetical</option>
                <option value="date_created">Date Created</option>
            </select>
            <button id="savePreferenceButton">Save Preference</button>

            <div id="saveMessage" style="color: green; margin-top: 10px;"></div>
        `;

        const sortSelect = document.getElementById("contactSortPreference");
        if (sortSelect) {
            sortSelect.value = profile.contact_sort_preference || "alphabetical";
        }

        const savePreferenceButton = document.getElementById("savePreferenceButton");
        if (savePreferenceButton) {
            savePreferenceButton.addEventListener("click", async () => {
                const newPreference = document.getElementById("contactSortPreference").value;

                const saveResponse = await fetch(`${API_URL}/users/profile`, {
                    method: "PUT",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ contact_sort_preference: newPreference })
                });

                if (saveResponse.ok) {
                    document.getElementById("saveMessage").innerText = "Preference saved!";
                    setTimeout(() => {
                        window.location.href = "/static/contacts.html"; // Redirect to contacts page
                    }, 1000); // slight delay to show message
                } else {
                    document.getElementById("saveMessage").innerText = "Error saving preference.";
                }
            });
        }
    }
}

// ------------------- CONTACT DETAIL PAGE -------------------
async function loadContactDetail() {
    const token = localStorage.getItem("token");
    const contactId = localStorage.getItem("selected_contact_id");

    const response = await fetch(`${API_URL}/contacts/${contactId}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.ok) {
        const contact = await response.json();
        const contactDiv = document.getElementById("contactDetails");
        contactDiv.innerHTML = `
            <p><strong>First Name:</strong> <input type="text" id="first_name" value="${contact.first_name}" disabled></p>
            <p><strong>Last Name:</strong> <input type="text" id="last_name" value="${contact.last_name || ""}" disabled></p>
            <p><strong>Company:</strong> <input type="text" id="company" value="${contact.company || ""}" disabled></p>
            <p><strong>Emails:</strong> <input type="text" id="emails" value="${(contact.emails || []).join(", ")}" disabled></p>
            <p><strong>Phone Numbers:</strong> <input type="text" id="phone_numbers" value="${(contact.phone_numbers || []).join(", ")}" disabled></p>
            <p><strong>Address:</strong> <input type="text" id="address" value="${contact.address || ""}" disabled></p>
            <p><strong>Birthday:</strong> <input type="date" id="birthday" value="${contact.birthday || ""}" disabled></p>
            <p><strong>Username:</strong> <input type="text" id="username" value="${contact.username || ""}" disabled></p>
            <p><strong>Other:</strong> <textarea id="notes" disabled>${contact.notes || ""}</textarea></p>
            <div id="saveEditDiv" style="margin-top: 10px;"></div>
        `;
    } else {
        alert("Failed to load contact details.");
    }
}

function redirectToNotes() {
    window.location.href = "/static/notes.html";
}

function enableEdit() {
    document.querySelectorAll("#contactDetails input, #contactDetails textarea").forEach(input => {
        input.disabled = false;
    });

    const saveDiv = document.getElementById("saveEditDiv");
    saveDiv.innerHTML = `<button onclick="saveContactChanges()">Save Changes</button>`;
}

async function saveContactChanges() {
    const token = localStorage.getItem("token");
    const contactId = localStorage.getItem("selected_contact_id");

    const updatedContact = {};

    const firstName = document.getElementById("first_name").value.trim();
    if (firstName) updatedContact.first_name = firstName;

    const lastName = document.getElementById("last_name").value.trim();
    if (lastName) updatedContact.last_name = lastName;

    const company = document.getElementById("company").value.trim();
    if (company) updatedContact.company = company;

    const emailsInput = document.getElementById("emails").value.trim();
    if (emailsInput) {
        const emailsArray = emailsInput.split(",").map(e => e.trim()).filter(e => e);

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const invalidEmails = emailsArray.filter(email => !emailRegex.test(email));

        if (invalidEmails.length > 0) {
            alert(`Invalid email(s) detected:\n\n${invalidEmails.join(", ")}\n\nPlease correct them before saving.`);
            return; // Stop the save
        }

        updatedContact.emails = emailsArray;
    }

    const phoneNumbers = document.getElementById("phone_numbers").value.trim();
    if (phoneNumbers) updatedContact.phone_numbers = phoneNumbers.split(",").map(p => p.trim()).filter(p => p);

    const address = document.getElementById("address").value.trim();
    if (address) updatedContact.address = address;

    const birthday = document.getElementById("birthday").value.trim();
    if (birthday) updatedContact.birthday = birthday;

    const username = document.getElementById("username").value.trim();
    if (username) updatedContact.username = username;

    const notes = document.getElementById("notes").value.trim();
    if (notes) updatedContact.notes = notes;

    if (Object.keys(updatedContact).length === 0) {
        alert("No changes detected to update!");
        return;
    }

    const response = await fetch(`${API_URL}/contacts/${contactId}`, {
        method: "PUT",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updatedContact)
    });

    if (response.ok) {
        alert("Contact updated successfully!");
        window.location.reload();
    } else {
        const errorData = await response.json();
        console.error("Update error:", errorData);
        alert("Failed to update contact. Please check your input.");
    }
}


async function deleteContact() {
    const token = localStorage.getItem("token");
    const contactId = localStorage.getItem("selected_contact_id");

    const confirmDelete = confirm("Are you sure you want to delete this contact?");
    if (!confirmDelete) return;

    const response = await fetch(`${API_URL}/contacts/${contactId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.ok) {
        alert("Contact deleted successfully!");
        window.location.href = "/static/contacts.html";
    } else {
        alert("Failed to delete contact.");
    }
}

// ------------------- LOGOUT -------------------
function logout() {
    localStorage.removeItem("token");
    window.location.href = "/static/index.html";
}

// ------------------- DOMContentLoaded Handling -------------------
document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("signupForm")) {
        document.getElementById("signupForm").addEventListener("submit", (e) => {
            e.preventDefault();
            const email = document.getElementById("signup_email").value;
            const password = document.getElementById("signup_password").value;
            signup(email, password);
        });
    }

    if (document.getElementById("loginForm")) {
        document.getElementById("loginForm").addEventListener("submit", (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            login(email, password);
        });
    }

    if (document.getElementById("contactList")) {
        loadContacts();
    }

    if (document.getElementById("contactDetails")) {
        loadContactDetail();
    }

    if (document.getElementById("noteList")) {
        const contactId = localStorage.getItem("selected_contact_id");
        loadContactName(contactId);   
        loadNotes();
    }

    if (document.getElementById("noteDetails")) {
        loadNoteDetail();
    }
    
    if (document.getElementById("noteForm")) {
        document.getElementById("noteForm").addEventListener("submit", (e) => {
            e.preventDefault();
            createNote();
        });
    }
    
    
    if (document.getElementById("profileInfo")) {
        loadProfile();
    }
});
