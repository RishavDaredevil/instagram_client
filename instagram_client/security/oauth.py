from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timezone, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Used openssl rand -hex 32
SECRET_KEY = '9235b15ad42677ad89df444d199dde911a1485a03624d1bd0a669eb16ede64af'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire,
                      "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:

        raise credentials_exception
    user = db_user.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user
