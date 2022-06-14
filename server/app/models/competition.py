from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .user_collection import UserCollection


class Competition(Base):
    title = Column(String(256), nullable=False)
    logo_url = Column(String(512), nullable=False)
    description = Column(String(2048), nullable=False)
    extra_credits = Column(Boolean, nullable=False)
    title_words = Column(String(256), nullable=False)
    category = Column(String(16), nullable=False)
    deadline = Column(DateTime, nullable=False)
    organizer = Column(String(256), nullable=False)
    level = Column(String(16), nullable=False)
    members_max = Column(Integer, nullable=False)
    home_page = Column(String(256), nullable=False)
    notice = Column(String(256), nullable=False)
    #
    teams = relationship(
        "Team", back_populates="competition", lazy="dynamic", cascade="all, delete", passive_deletes=True
    )
    comments = relationship(
        "Comment", back_populates="competition", lazy="dynamic", cascade="all, delete", passive_deletes=True
    )
    collected_users = relationship(
        "User", secondary=UserCollection, back_populates="collections", lazy="dynamic", passive_deletes=True
    )
