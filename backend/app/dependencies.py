# dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import decode_access_token  # Import the JWT decoding function
from app.schemas import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Decodes the JWT token and returns the current user.
    This is used to validate the user making the request.
    """
    # Decode the token to extract the user_id (sub)
    username = decode_access_token(token)
    
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token"
        )
    
    # Query the database for the user
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
