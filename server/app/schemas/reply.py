from datetime import date

from pydantic import BaseModel

from .user import User


class ReplyCreate(BaseModel):
    msg: str


class Reply(BaseModel):
    id: int
    msg: str
    time: date
    user: User

    class Config:
        orm_mode = True
