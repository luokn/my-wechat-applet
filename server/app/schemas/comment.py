from datetime import date
from typing import List

from pydantic import BaseModel

from .reply import Reply
from .user import User


class CommentCreate(BaseModel):
    msg: str


class Comment(BaseModel):
    id: int
    msg: str
    time: date
    user: User
    replies: List[Reply]

    class Config:
        orm_mode = True
