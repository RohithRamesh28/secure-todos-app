from __future__ import annotations
import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List


# ----------- Note Schemas -----------
class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    # NoteCreate will inherit from NoteBase
    is_pinned: Optional[bool] = False 
    pass
 # Default value for is_pinned


class NoteOut(NoteBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None  

    is_pinned: bool  

    class Config:   
        orm_mode = True  


# ----------- User Schemas -----------
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str


class UserOut(UserBase):
    id: int
    username: str
    notes: List[NoteOut] = []  

    class Config:
        orm_mode = True


# ----------- Token Schema -----------
class Token(BaseModel):
    access_token: str
    token_type: str
