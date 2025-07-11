import datetime
from sqlalchemy.orm import Session

from .models import DbInstaLikes


def get_all_likes(db: Session):
    return db.query(DbInstaLikes).all()

def create_like(db: Session, user_id: int, post_id: int):
    new_like = DbInstaLikes(
        user_id=user_id,
        post_id=post_id,
    )
    new_like.created_at = datetime.datetime.now(datetime.timezone.utc)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like

# def get_like_by_likename(db: Session, likename: str):
#     like = db.query(DbInstaLikes).filter(DbInstaLikes.likename == likename).first()
#     return like
#
# def get_like_by_id(db: Session, id: int):
#     like = db.query(DbInstaLikes).filter(DbInstaLikes.id == id)
#     return like


def delete_like_by_id(db: Session, like_id: int):
    db.query(DbInstaLikes).filter(DbInstaLikes.like_id == like_id).delete()
    db.commit()
    return None

# Add this new function to the file
def delete_like_by_post_and_user(db: Session, post_id: int, user_id: int):
    """Deletes a like based on the post and user who liked it."""
    like_to_delete = db.query(DbInstaLikes).filter(
        DbInstaLikes.post_id == post_id,
        DbInstaLikes.user_id == user_id
    ).first()

    if like_to_delete:
        db.delete(like_to_delete)
        db.commit()
        return True # Indicate success
    return False # Indicate like was not found

