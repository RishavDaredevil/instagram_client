from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .oauth import create_access_token
from ..db.database import get_db
from ..db import db_user
from ..db.hashing_fn import verify_password

db_dependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/login", tags=["authentication"])

@router.post("")
def login(db: db_dependency, user:  Annotated[OAuth2PasswordRequestForm, Depends()]):
    existing_user = db_user.get_user_by_username(db=db, username=user.username)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    if not verify_password(plain_password=user.password, hashed_password=existing_user.password):
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    data_token: Dict[str, str] = {
        "sub": str(existing_user.id),
        "username": existing_user.username,
    }
    access_token = create_access_token(data=data_token)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": existing_user.username
    }
