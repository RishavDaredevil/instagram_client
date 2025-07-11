import shutil
from typing import List, Annotated
from fastapi import APIRouter, File, UploadFile, Depends, Form, status, HTTPException
from fastapi import Path as fastapi_path
from sqlalchemy.orm import Session
from pathlib import Path

from ..db import db_post, db_comment, db_like
from ..db.database import get_db
from ..schema import InstaPost, InstaPostResponse, UserInput, CommentOutput, CommentInput, LikeOutput
from ..security.oauth import get_current_user


BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR / "post_images"

router = APIRouter(prefix="/post", tags=["post"])

db_dependency = Annotated[Session, Depends(get_db)]
post_form_param = Annotated[str, Form(...)]


@router.get("s", response_model=List[InstaPostResponse], status_code=status.HTTP_200_OK)
def read_blog_posts(db: db_dependency):
    blog_posts = db_post.get_all_insta_post(db=db)
    return blog_posts


@router.post("", response_model=InstaPostResponse, status_code=status.HTTP_201_CREATED)
def create_blog_post(
        db: db_dependency,
        user: Annotated[UserInput, Depends(get_current_user)],
        caption: post_form_param = "content1",
        image_file: UploadFile = File(...)
):
    image_path = path / image_file.filename
    with open(image_path, "w+b") as f:
        shutil.copyfileobj(image_file.file, f)

    # Path to be used in the HTML src attribute
    image_url = f"/post_images/{image_file.filename}"

    request = InstaPost(username=user.username, caption=caption)
    blog_post = db_post.create_insta_post(db=db, request=request, image_path=image_url)
    return blog_post

@router.put("/{post_id}", response_model=InstaPostResponse)
def update_post_by_post_id(
        db: db_dependency,
        post_id: Annotated[int, fastapi_path(gt=0)],
        user: Annotated[UserInput, Depends(get_current_user)],
        caption: post_form_param = "content1",
        image_file: Annotated[UploadFile | str | None , File()] = None
):
    # Fetch the existing post from the database
    existing_post = db_post.get_post_by_id(db=db, post_id=post_id)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    image_url = existing_post.image_path  # Default to the existing image path

    # 2. Use isinstance() to check if a real file was uploaded.
    # This will be True only for an actual file, not for "" or None.
    if isinstance(image_file, UploadFile):
        # If a new file is provided, save it and update the URL
        image_path = path / image_file.filename
        with open(image_path, "w+b") as f:
            shutil.copyfileobj(image_file.file, f)
        image_url = f"/post_images/{image_file.filename}"

    # Prepare the update request and execute
    request = InstaPost(username=user.username, caption=caption)
    updated_post = db_post.update_post(db=db, request=request, image_path=image_url, post_id=post_id)

    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: Annotated[int, fastapi_path(gt=0)], db: db_dependency):
    db_post.delete_insta_post(id=post_id, db=db)

# Comment functionality

@router.post("/{post_id}/comment", response_model=CommentOutput, status_code=status.HTTP_201_CREATED,tags=["comment"])
def create_comment(
        db: db_dependency,
        user: Annotated[UserInput, Depends(get_current_user)],
        post_id: Annotated[int,Path(gt=0)],
        caption: CommentInput
):
    comment = db_comment.create_comment(db=db, caption=caption.caption, post_id=post_id, user_id=user.id)
    return comment


@router.put("/{post_id}/comment/{comment_id}", response_model=CommentOutput,tags=["comment"])
def update_comment(db: db_dependency, caption: CommentInput, comment_id: Annotated[int,Path(gt=0)],
                   user: Annotated[UserInput, Depends(get_current_user)]):
    comment = db_comment.update_comment(db=db, caption=caption.caption, comment_id=comment_id)
    return comment


@router.delete("/{post_id}/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT,tags=["comment"])
def delete_post(comment_id: int, db: db_dependency):
    db_comment.delete_comment_by_id(comment_id=comment_id, db=db)


# Like functionality
@router.post("/{post_id}/like", response_model=LikeOutput, status_code=status.HTTP_201_CREATED,tags=["like"])
def create_like(
        db: db_dependency,
        user: Annotated[UserInput, Depends(get_current_user)],
        post_id: Annotated[int,Path(gt=0)],
):
    like = db_like.create_like(db=db, post_id=post_id, user_id=user.id)
    return like


# Add this new endpoint and remove the old like-deletion endpoint
@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT, tags=["like"])
def delete_like(
        post_id: int,
        db: db_dependency,
        user: Annotated[UserInput, Depends(get_current_user)]
):
    """Deletes a like for a given post by the current authenticated user."""
    success = db_like.delete_like_by_post_and_user(db=db, post_id=post_id, user_id=user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found.")
    # On success, return no content