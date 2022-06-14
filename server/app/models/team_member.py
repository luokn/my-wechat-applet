from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

TeamMember = Table(
    "team_member",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("team.id", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE")),
)
