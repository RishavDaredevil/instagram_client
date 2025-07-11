import datetime
from sqlalchemy.orm import Session

from .models import DbInstaComment
from ..schema import CommentInput


def get_all_comments(db: Session):
    return db.query(DbInstaComment).all()

def create_comment(db: Session, caption: str, user_id: int, post_id: int):
    new_comment = DbInstaComment(
        caption=caption,
        user_id=user_id,
        post_id=post_id,
    )
    new_comment.created_at = datetime.datetime.now(datetime.timezone.utc)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# def get_comment_by_commentname(db: Session, commentname: str):
#     comment = db.query(DbInstaComment).filter(DbInstaComment.commentname == commentname).first()
#     return comment
#
# def get_comment_by_id(db: Session, id: int):
#     comment = db.query(DbInstaComment).filter(DbInstaComment.id == id)
#     return comment

def update_comment(db: Session,  caption: str, comment_id: int):
    comment_to_update = db.query(DbInstaComment).filter(DbInstaComment.comment_id == comment_id).first()
    if comment_to_update:
        comment_to_update.caption = caption
    db.commit()
    db.refresh(comment_to_update)
    return comment_to_update

def delete_comment_by_id(db: Session, comment_id: int):
    db.query(DbInstaComment).filter(DbInstaComment.comment_id == comment_id).delete()
    db.commit()
    return None


