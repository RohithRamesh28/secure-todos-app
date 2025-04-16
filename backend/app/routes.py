from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.auth import verify_password, hash_password, create_access_token
from app.schemas import Token, UserCreate
from app.models import User
from app import crud_routes
from app.dependencies import get_current_user 
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, dependencies
from app.schemas import NoteCreate, NoteOut




router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ----------- Login Route -----------
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
 
    user = db.query(User).filter(User.username == form_data.username).first()

 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Check if the password is correct
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate an access token for the authenticated user
    access_token = create_access_token(data={"sub": user.username})

    # Return the token response
    return {"access_token": access_token, "token_type": "bearer"}


# ----------- Register Route -----------
@router.post("/register", response_model=Token)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = db.query(User).filter(User.email == user_create.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password before storing it
    hashed_password = hash_password(user_create.password)

    # Create a new user instance
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )

    # Add the new user to the database
    db.add(new_user)
    db.commit()

    # Generate an access token for the newly registered user
    access_token = create_access_token(data={"sub": new_user.username})

    # Return the token response
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/notes/", response_model=NoteOut)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_routes.create_note(note, db, current_user.id)

# --- READ all notes ---
@router.get("/notes/", response_model=List[NoteOut])
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_routes.get_notes(db, current_user.id)

# --- READ a single note ---
@router.get("/{note_id}/", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_routes.get_note(note_id, db, current_user.id)

# --- UPDATE a note ---
@router.put("/{note_id}/", response_model=NoteOut)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_routes.update_note(note_id, note, db, current_user.id)

# --- DELETE a note ---
@router.delete("/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_routes.delete_note(note_id, db, current_user.id)

#search by query
@router.get("/notes/search/", response_model=List[schemas.NoteOut])
def search_notes(query: str = Query(..., min_length=1), db: Session = Depends(get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    notes = db.query(models.Note).filter(
        models.Note.owner_id == current_user.id,
        (models.Note.title.ilike(f"%{query}%")) | (models.Note.content.ilike(f"%{query}%"))
    ).all()

    return notes

@router.patch("/notes/{note_id}/pin/", response_model=schemas.NoteOut)
def pin_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.is_pinned = True
    db.commit()
    db.refresh(note)
    return note

@router.patch("/notes/{note_id}/unpin/", response_model=schemas.NoteOut)
def unpin_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.is_pinned = False
    db.commit()
    db.refresh(note)
    return note
    
@router.get("/notes/pinned/", response_model=list[NoteOut])
def get_pinned_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(models.Note).filter(
        models.Note.owner_id == current_user.id,
        models.Note.is_pinned == True
    ).all()

@router.get("/notes/unpinned/", response_model=list[NoteOut])
def get_unpinned_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(models.Note).filter(
        models.Note.owner_id == current_user.id,
        models.Note.is_pinned == False
    ).all()