import re
import datetime
from typing import Optional
from pydantic import FilePath
from sqlalchemy.orm import Session

from .models import DbUser
from ..schema import UserInput, UserOutput, UpdatingUserInput
from .hashing_fn import get_password_hash

def get_all_users(db: Session):
    return db.query(DbUser).all()

def create_user(db: Session, user: UserInput, profile_pic_path: FilePath):
    new_user = DbUser(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        bio=user.bio,
    )
    new_user.profile_pic_path = profile_pic_path
    new_user.created_at = datetime.datetime.now(datetime.timezone.utc)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    return user

def get_user_by_id(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    return user

def search_users_by_username(db: Session, query: str):
    """
    Searches for users with usernames that contain the query string.
    The search is case-insensitive.
    """
    query = query.strip()

    escaped_query = re.sub(r'([%_])', r'\\\1', query)
    return db.query(DbUser).filter(DbUser.username.ilike(f"%{escaped_query}%", escape='\\')).order_by(DbUser.username).limit(10).all()


def update_user(db: Session, user: UpdatingUserInput,username: str, profile_pic_path: Optional[FilePath]):
    user_to_update = db.query(DbUser).filter(DbUser.username == username).first()
    if user_to_update:
        user_to_update.profile_pic_path = profile_pic_path
        user_to_update.email = user.email
        user_to_update.bio = user.bio
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

def update_user_password(db: Session, user: UserInput, password: str):
    user_to_update = db.query(DbUser).filter(DbUser.username == user.username).first()
    if user_to_update:
        user_to_update.password = get_password_hash(password)
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

def delete_user_by_id(db: Session, user_id: int):
    db.query(DbUser).filter(DbUser.id == user_id).delete()
    db.commit()
    return None


