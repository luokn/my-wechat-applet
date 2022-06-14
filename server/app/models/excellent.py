from sqlalchemy import Column, String

from .base import Base


class Excellent(Base):
    name = Column(String(64), nullable=False)
    captain = Column(String(64), nullable=False)
    members = Column(String(64), nullable=False)
    introduce = Column(String(512), nullable=False)
