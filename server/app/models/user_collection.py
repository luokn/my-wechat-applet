from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

UserCollection = Table(
    "user_collection",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE")),
    Column("competition_id", Integer, ForeignKey("competition.id", ondelete="CASCADE")),
)
