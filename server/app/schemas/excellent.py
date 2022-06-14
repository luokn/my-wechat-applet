from typing import Optional

from pydantic import BaseModel


class ExcellentCreate(BaseModel):
    name: str
    captain: str
    members: str
    introduce: str


class ExcellentUpdate(BaseModel):
    name: Optional[str]
    captain: Optional[str]
    members: Optional[str]
    introduce: Optional[str]


class Excellent(BaseModel):
    id: int
    name: str
    captain: str
    members: str
    introduce: str

    class Config:
        orm_mode = True
