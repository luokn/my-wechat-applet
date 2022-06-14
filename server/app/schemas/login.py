from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class Login(BaseModel):
    username: Optional[str]
    password: Optional[str]
    code: Optional[str]
    avatar: Optional[str]
    grant_type: str

    @classmethod
    def form(
        cls,
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        code: Optional[str] = Form(None),
        avatar: Optional[str] = Form(None),
        grant_type: str = Form("password"),
    ):
        return cls(username=username, password=password, code=code, avatar=avatar, grant_type=grant_type)
