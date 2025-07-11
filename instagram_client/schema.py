from typing import List, Optional

from fastapi import Path
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.annotation import Annotated

# Schemas for Users
class UserInput(BaseModel):
    username: str
    password: str
    email: str
    bio: Optional[str]
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "user1",
                "email": "email1",
                "password": "password1",
                "bio": "bio1",
            }
        }
    }

class UserOutput(BaseModel):
    username: str
    email: str
    bio: str
    profile_pic_path: str
    model_config = ConfigDict(from_attributes=True)

class UpdatingUserInput(BaseModel):
    email: str
    bio: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "updated_email1",
                "bio": "updated_bio1",
            }
        }
    }

# Schemas for Posts
class InstaPost(BaseModel):
    username: str
    caption: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "caption": "Great Holiday in Japan",
            }
        }
    }

class User(BaseModel):
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class InstaPostComment(BaseModel):
    caption: str
    user: User
    model_config = ConfigDict(from_attributes=True)

class InstaPostLike(BaseModel):
    like_id: int
    model_config = ConfigDict(from_attributes=True)

class InstaPostResponse(BaseModel):
    user : User
    caption: str
    comments: List[InstaPostComment]
    likes: List[InstaPostLike]

    model_config = ConfigDict(from_attributes=True)

# Schemas for Comments
class CommentInput(BaseModel):
    caption: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "caption": "Great Holiday in Japan",
            }
        }
    }

class Post(BaseModel):
    post_id: int
    caption: str
    model_config = ConfigDict(from_attributes=True)

class CommentOutput(BaseModel):
    caption: str
    user: User
    post: Post
    model_config = ConfigDict(from_attributes=True)

# Schemas for Likes

class LikeOutput(BaseModel):
    like_id: int
    user_id: int
    post_id: int
    model_config = ConfigDict(from_attributes=True)
