# crud_routes.py

from sqlalchemy.orm import Session
from app.models import Note, User
from app.schemas import NoteCreate
from fastapi import HTTPException, status

# --- CREATE a note ---
def create_note(note: NoteCreate, db: Session, owner_id: int):
  
    db_note = Note(
        title=note.title,
        content=note.content,
        owner_id=owner_id,
        is_pinned=note.is_pinned if note.is_pinned is not None else False  # Default is False
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# --- READ all notes ---
def get_notes(db: Session, owner_id : int):
    notes = db.query(Note).filter(Note.owner_id  == owner_id ).all()
    return notes

# --- READ a single note ---
def get_note(note_id: int, db: Session, owner_id : int):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id  == owner_id ).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

# --- UPDATE a note ---
def update_note(note_id: int, note: NoteCreate, db: Session, owner_id : int):
    db_note = db.query(Note).filter(Note.id == note_id, Note.owner_id  == owner_id ).first()
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

# --- DELETE a note ---
def delete_note(note_id: int, db: Session, owner_id : int):
    db_note = db.query(Note).filter(Note.id == note_id, Note.owner_id  == owner_id ).first()
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"detail": "Note deleted successfully"}
