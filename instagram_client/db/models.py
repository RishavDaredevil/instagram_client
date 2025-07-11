# In instagram_client/db/models.py

import datetime
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from .database import Base


class DbUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    bio = Column(String)
    profile_pic_path = Column(String)
    posts: Mapped[List["DbInstaPost"]] = relationship(back_populates="user")
    comments: Mapped[List["DbInstaComment"]] = relationship(back_populates="user")
    likes: Mapped[List["DbInstaLikes"]] = relationship(back_populates="user")


class DbInstaPost(Base):
    __tablename__ = 'insta_posts'

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    caption = Column(String, nullable=False)
    image_path = Column(String)
    timestamp = Column(DateTime)

    user: Mapped["DbUser"] = relationship(back_populates="posts")
    comments: Mapped[List["DbInstaComment"]] = relationship(back_populates="post")
    # This relationship is now bidirectional
    likes: Mapped[List["DbInstaLikes"]] = relationship(back_populates="post")


class DbInstaComment(Base):
    __tablename__ = 'insta_comments'

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('insta_posts.post_id'), nullable=False)
    timestamp = Column(DateTime)
    user: Mapped["DbUser"] = relationship(back_populates="comments")
    post: Mapped["DbInstaPost"] = relationship(back_populates="comments")


class DbInstaLikes(Base):
    __tablename__ = 'insta_likes'

    like_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('insta_posts.post_id'), nullable=False)
    timestamp = Column(DateTime)
    user: Mapped["DbUser"] = relationship(back_populates="likes")
    # This relationship is now bidirectional
    post: Mapped["DbInstaPost"] = relationship(back_populates="likes")
