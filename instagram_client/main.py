from fastapi import FastAPI
from starlette import status
from starlette.staticfiles import StaticFiles
from pathlib import Path

# Import the new login_page router
from .routers import user, insta_post, creating_comment, creating_like, user_page, instagram_post_page, login_page
from .security import auth_router
from .db import models
from .db.database import engine

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "profile_pics"
path_insta_post = BASE_DIR / "post_images"
app = FastAPI()

# Include the new routers
app.include_router(login_page.router) # For serving the login page
app.include_router(auth_router.router) # For handling the POST /login request
app.include_router(user.router)
app.include_router(insta_post.router)
app.include_router(creating_comment.router)
app.include_router(creating_like.router)
app.include_router(user_page.router)
app.include_router(instagram_post_page.router)


models.Base.metadata.create_all(bind=engine)

# Change the root path to redirect to the login page
@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

app.mount("/profile_pics", StaticFiles(directory=path), name="profile_pics")
app.mount("/post_images", StaticFiles(directory=path_insta_post), name="post_images")