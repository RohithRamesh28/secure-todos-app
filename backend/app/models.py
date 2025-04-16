from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notes = relationship('Note', back_populates='owner') 

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id')) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_pinned = Column(Boolean, nullable=False, default=False) 


    owner = relationship('User', back_populates='notes') 
