from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

from ..db import db_user
from ..db.database import get_db

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'template')))
db_dependency = Annotated[Session, Depends(get_db)]

# Corrected prefix as requested
router = APIRouter(prefix="/user_page", tags=["user_page"])


@router.get("/{username}", response_class=HTMLResponse)
async def get_user_page(request: Request, username: str, db: db_dependency):
    user = db_user.get_user_by_username(db, username=username)
    if not user:
        # You might want to handle the case where the user is not found
        return HTMLResponse(status_code=404, content="<h1>User not found</h1>")

    # Ensure posts are loaded correctly, assuming a relationship 'posts' exists
    # The template expects user.posts to be iterable
    return templates.TemplateResponse(
        "user_page.html",
        {"request": request, "user": user}
    )