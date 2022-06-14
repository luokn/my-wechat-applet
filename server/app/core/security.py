from datetime import datetime, timedelta
from typing import Optional, Dict

from jose import JWTError, jwt

from .config import settings


def encode_token(claims: Dict[str, str]) -> str:
    claims["exp"] = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRE_DAYS)
    return jwt.encode(claims, settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> Optional[Dict[str, str]]:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
