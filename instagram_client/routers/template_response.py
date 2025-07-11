from typing import Annotated
from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session
from starlette.requests import Request
from ..db.database import get_db
from ..db import db_post

BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR / "template"
router = APIRouter(prefix="/template", tags=["template"])

templates = Jinja2Templates(directory=path)
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_class=HTMLResponse)
async def blog_page(request: Request, db: db_dependency, page: int = Query(1, gt=0)):
    page_size = 10
    skip = (page - 1) * page_size
    posts, total_count = db_post.get_posts_for_frontend(db, skip=skip, limit=page_size)

    total_pages = (total_count + page_size - 1) // page_size

    return templates.TemplateResponse(
        "blog_page.html",
        {
            "request": request,
            "posts": posts,
            "current_page": page,
            "total_pages": total_pages,
        },
    )