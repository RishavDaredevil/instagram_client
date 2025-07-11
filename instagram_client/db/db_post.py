import datetime
from pydantic import FilePath
from sqlalchemy.orm import Session, selectinload

from .models import DbInstaPost, DbInstaComment, DbInstaLikes
from .db_user import get_user_by_username
from ..schema import InstaPost

def create_insta_post(request, db: Session, image_path: FilePath):
    user_det = get_user_by_username(db, request.username)
    new_insta_post = DbInstaPost(
        caption=request.caption,
        user_id=user_det.id
    )
    new_insta_post.timestamp = datetime.datetime.now(datetime.timezone.utc)
    new_insta_post.image_path = image_path
    db.add(new_insta_post)
    db.commit()
    db.refresh(new_insta_post)
    return new_insta_post

def get_all_insta_post(db: Session):
    all_post = (
        db.query(DbInstaPost)
        .options(
            # Eagerly load the post's author
            selectinload(DbInstaPost.user),
            # Eagerly load the comments and their respective authors
            selectinload(DbInstaPost.comments).joinedload(DbInstaComment.user),
            # Eagerly load the likes and their respective authors
            selectinload(DbInstaPost.likes).joinedload(DbInstaLikes.user)
        )
        .order_by(DbInstaPost.timestamp.desc())
    )
    return all_post

def get_post_by_id(db: Session, post_id: int):
    post = db.query(DbInstaPost).filter(DbInstaPost.post_id == post_id).first()
    return post

def update_post(db: Session, request: InstaPost, post_id: int, image_path: FilePath):
    user_to_update = db.query(DbInstaPost).filter(DbInstaPost.post_id == post_id).first()
    if user_to_update:
        user_to_update.image_path = image_path
        user_to_update.caption = request.caption
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

def delete_insta_post(db: Session, id: int):
    db.query(DbInstaPost).filter(DbInstaPost.post_id == id).delete()
    db.commit()
    return None

def get_posts_for_frontend(db: Session, skip: int = 0, limit: int = 10):
    posts = (
        db.query(DbInstaPost)
        .options(
            selectinload(DbInstaPost.comments),
            selectinload(DbInstaPost.likes)
        )
        .order_by(DbInstaPost.timestamp.desc())
        .offset(skip).limit(limit).all()
    )
    total_count = db.query(DbInstaPost).count()
    return posts, total_count