from datetime import date
from typing import Optional

from pydantic import BaseModel

from .user import User


class TeamCreate(BaseModel):
    name: str
    deadline: Optional[date]
    introduce: Optional[str]
    requirements: Optional[str]


class TeamUpdate(BaseModel):
    name: Optional[str]
    deadline: Optional[date]
    introduce: Optional[str]
    requirements: Optional[str]


class Team(BaseModel):
    id: int
    name: str
    captain: User
    competition_id: int
    deadline: Optional[date]
    introduce: Optional[str]
    requirements: Optional[str]

    class Config:
        orm_mode = True
