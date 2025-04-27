# app/utils/normalization.py

def normalize_note_fields(note_data: dict) -> dict:
    """
    Normalize inbound note fields to ensure 'body' is present.
    Accepts note_body, note_text alternatives.
    """
    if "note_body" in note_data and "body" not in note_data:
        note_data["body"] = note_data.pop("note_body")
    if "note_text" in note_data and "body" not in note_data:
        note_data["body"] = note_data.pop("note_text")
    return note_data

def normalize_contact_fields(contact_data: dict) -> dict:
    """
    Normalize inbound contact fields.
    - Accepts fname/lname as first_name/last_name
    - Converts emails/phone_numbers from strings to lists if necessary
    """
    # Map alternative field names
    if "fname" in contact_data and "first_name" not in contact_data:
        contact_data["first_name"] = contact_data.pop("fname")
    if "lname" in contact_data and "last_name" not in contact_data:
        contact_data["last_name"] = contact_data.pop("lname")

    # Normalize emails
    if "emails" in contact_data:
        if isinstance(contact_data["emails"], str):
            contact_data["emails"] = [email.strip() for email in contact_data["emails"].split(",") if email.strip()]

    # Normalize phone_numbers
    if "phone_numbers" in contact_data:
        if isinstance(contact_data["phone_numbers"], str):
            contact_data["phone_numbers"] = [phone.strip() for phone in contact_data["phone_numbers"].split(",") if phone.strip()]

    return contact_data

def normalize_user_fields(user_data: dict) -> dict:
    """
    Normalize inbound user fields.
    - Lowercase emails
    - Strip whitespace from email and username
    """
    if "email" in user_data and isinstance(user_data["email"], str):
        user_data["email"] = user_data["email"].strip().lower()

    if "username" in user_data and isinstance(user_data["username"], str):
        user_data["username"] = user_data["username"].strip()

    return user_data
