from typing import List, Optional
from pydantic import BaseModel


class UserUpdate(BaseModel):
    username: Optional[str]
    introduce: Optional[str]
    phone_number: Optional[str]
    wechat_number: Optional[str]
    major: Optional[str]
    degree: Optional[str]
    gender: Optional[str]


class Competition(BaseModel):
    id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
    avatar: Optional[str]
    introduce: Optional[str]
    phone_number: Optional[str]
    wechat_number: Optional[str]
    major: Optional[str]
    degree: Optional[str]
    gender: Optional[str]

    collections: List[Competition]

    class Config:
        orm_mode = True


class IdentityUser(User):
    is_admin: bool
    is_superadmin: bool
