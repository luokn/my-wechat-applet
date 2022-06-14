from typing import Optional
from pydantic import BaseModel
from datetime import date


class BaseCompetition(BaseModel):
    title: str
    logo_url: str
    description: str
    extra_credits: bool
    category: str
    deadline: date
    organizer: str
    level: str
    members_max: int
    home_page: str
    notice: str


class CompetitionCreate(BaseCompetition):
    ...


class CompetitionUpdate(BaseCompetition):
    title: Optional[str]
    logo_url: Optional[str]
    description: Optional[str]
    multi_members: Optional[bool]
    extra_credits: Optional[bool]
    category: Optional[str]
    deadline: Optional[date]
    organizer: Optional[str]
    level: Optional[str]
    members_max: Optional[int]
    home_page: Optional[str]
    notice: Optional[str]


class Competition(BaseCompetition):
    id: int

    class Config:
        orm_mode = True
