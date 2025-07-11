from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pathlib import Path

from ..db import db_like, db_user
from ..db.database import get_db
from ..schema import LikeOutput

router = APIRouter(prefix="/like",tags=["like"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("s", response_model=List[LikeOutput], status_code=status.HTTP_200_OK)
def read_likes(db: db_dependency):
    likes = db_like.get_all_likes(db=db)
    return likes

