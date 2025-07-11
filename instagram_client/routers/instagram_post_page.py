from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

from ..db import db_post, db_user # Import db_user
from ..db.database import get_db

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'template')))
db_dependency = Annotated[Session, Depends(get_db)]

# The prefix was updated as you requested
router = APIRouter(prefix="/instagram_posts", tags=["post_page"])

@router.get("/", response_class=HTMLResponse)
async def get_instagram_post_page(request: Request, db: db_dependency):
    # Fetch all posts and all users from the database
    posts = db_post.get_all_insta_post(db).all()
    all_users = db_user.get_all_users(db) # Fetch all users
    return templates.TemplateResponse(
        "instagram_post_page.html",
        {
            "request": request,
            "posts": posts,
            "all_users": all_users # Pass the list of users to the template
        }
    )