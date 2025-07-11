from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Setup templates directory
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'template')))

# The prefix is empty so the path will be "/"
router = APIRouter(tags=["authentication"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Serves the main login page.
    """
    return templates.TemplateResponse("login_page.html", {"request": request})