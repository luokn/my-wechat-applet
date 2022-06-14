from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

TeamApplication = Table(
    "team_application",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("team.id", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE")),
)
