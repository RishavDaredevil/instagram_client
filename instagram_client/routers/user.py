import logging
import shutil
from typing import List, Annotated, Optional
from fastapi import APIRouter, File, UploadFile, Depends, Form, status, HTTPException, Query
from fastapi import Path as fastapi_path
from sqlalchemy.orm import Session
from pathlib import Path

from ..db import db_user
from ..db.database import get_db
from ..schema import UserInput, UserOutput, UpdatingUserInput
from ..security.oauth import get_current_user

BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR / "profile_pics"

router = APIRouter(prefix="/user", tags=["user"])

db_dependency = Annotated[Session, Depends(get_db)]
user_form_param = Annotated[str, Form(...)]
optional_form_param = Annotated[str|None, Form()]

@router.post("", response_model=UserOutput)
async def create_user(username: user_form_param,password: user_form_param,
                      email: user_form_param, db: db_dependency,
                      bio: optional_form_param = None, profile_pic: UploadFile = File(...)):
    image_path = path / profile_pic.filename
    with open(image_path, "w+b") as f:
        shutil.copyfileobj(profile_pic.file, f)

    # Path to be used in the HTML src attribute
    image_url = f"/profile_pics/{profile_pic.filename}"

    user_input = UserInput(username=username, password=password, email=email, bio=bio)
    new_user = db_user.create_user(db=db,user= user_input, profile_pic_path=image_url)
    return new_user

@router.get("s", response_model=List[UserOutput])
def read_users(db: db_dependency, user_auth : Annotated[UserInput,Depends(get_current_user)]):
    return db_user.get_all_users(db=db)

@router.get("/{username}", response_model=UserOutput)
def read_user_by_username(username: str,db: db_dependency, user_auth : Annotated[UserInput,Depends(get_current_user)]):
    return db_user.get_user_by_username(db=db, username=username)

@router.put("/{username}", response_model=UserOutput)
def update_user_by_username(db: db_dependency,username: Annotated[str, fastapi_path(min_length=5)],
                            bio: optional_form_param = None, email: optional_form_param = None,
                            profile_pic: Annotated[UploadFile | str | None , File()] = None):
    # Fetch the existing post from the database
    existing_user_det = db_user.get_user_by_username(db=db, username=username)
    if not existing_user_det:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if bio is None:
        bio = existing_user_det.bio
    if email is None:
        email = existing_user_det.email
    image_url = existing_user_det.profile_pic_path  # Default to the existing image path

    # 2. Use isinstance() to check if a real file was uploaded.
    # This will be True only for an actual file, not for "" or None.
    if isinstance(profile_pic, UploadFile):
        # If a new file is provided, save it and update the URL
        profile_pic_path = path / profile_pic.filename
        with open(profile_pic_path, "w+b") as f:
            shutil.copyfileobj(profile_pic.file, f)
        image_url = f"/post_images/{profile_pic.filename}"

    user_input = UpdatingUserInput(email=email, bio=bio)
    updated_user = db_user.update_user(db=db, user=user_input,username=username, profile_pic_path=image_url)
    return updated_user

@router.delete("/{username}", status_code= status.HTTP_204_NO_CONTENT)
def delete_user(username: str, db: db_dependency):
    user_to_del = db_user.get_user_by_username(db=db, username=username)
    return db_user.delete_user_by_id(db=db, user_id= user_to_del.id)


@router.get("s/search", response_model=List[UserOutput])
def search_users(
        db: db_dependency,
        user_auth: Annotated[UserInput, Depends(get_current_user)],
        query: Annotated[str|None, Query(min_length= 1)] = None
):
    """
    Endpoint to search for users. Now uses the dedicated db_user function.
    """
    print(f"Searching for {query}")
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No query provided")

    # 1. Call the new function from db_user to get database objects
    db_users = db_user.search_users_by_username(db, query)

    return db_users

