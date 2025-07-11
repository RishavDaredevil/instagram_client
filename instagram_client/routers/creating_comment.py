from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pathlib import Path

from ..db import db_comment, db_user
from ..db.database import get_db
from ..schema import CommentOutput, CommentInput, UserInput
from ..security.oauth import get_current_user

router = APIRouter(prefix="/comment",tags=["comment"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("s", response_model=List[CommentOutput], status_code=status.HTTP_200_OK)
def read_comments(user: Annotated[UserInput, Depends(get_current_user)],db: db_dependency,):
    comments = db_comment.get_all_comments(db=db)
    return comments
