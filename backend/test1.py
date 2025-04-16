from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Note
from app.schemas import NoteCreate
from app.main import app  # Assuming your FastAPI app is defined in main.py
from fastapi.testclient import TestClient
from app.database import SessionLocal  # Assuming you have a SessionLocal to interact with DB


def create_note(note: NoteCreate, db: Session, owner_id: int):
    db_note = Note(
        title=note.title,
        content=note.content,
        owner_id=owner_id,
        is_pinned=note.is_pinned  # Assuming is_pinned is part of NoteCreate schema
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    # Check the value of is_pinned after creation and log it
    if db_note.is_pinned is None:
        print(f"Note '{db_note.title}' is_pinned is None.")
    elif db_note.is_pinned:
        print(f"Note '{db_note.title}' is_pinned is True.")
    else:
        print(f"Note '{db_note.title}' is_pinned is False.")
    
    return db_note


# TEST CASE: Testing the create_note function directly

def test_create_note_with_is_pinned():
    # Create a mock db session (you should use a test DB, e.g., SQLite in-memory)
    db = SessionLocal()  # Initialize a new session

    # Define the input note data
    note_data = {
        "title": "Test Note",
        "content": "This is a test note.",
        "is_pinned": True  # Change to False or None to test other scenarios
    }

    # Create the NoteCreate schema instance
    note_create = NoteCreate(**note_data)

    # Call the create_note function with test data
    created_note = create_note(note_create, db, owner_id=1)

    # Check if the created note has the correct `is_pinned` value
    assert created_note.is_pinned == note_data["is_pinned"], f"Expected is_pinned to be {note_data['is_pinned']} but got {created_note.is_pinned}."

    print("Test Passed: Note was created successfully.")

# Run the test manually
if __name__ == "__main__":
    test_create_note_with_is_pinned()

