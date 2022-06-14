from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base
from .team_application import TeamApplication
from .team_member import TeamMember
from .user_collection import UserCollection


class User(Base):
    username = Column(String(256), nullable=False)
    openid = Column(String(256), index=True, unique=True, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_superadmin = Column(Boolean, nullable=False)
    avatar = Column(String(256), nullable=True)
    username_words = Column(String(256), nullable=True)
    introduce = Column(String(1024), nullable=True)
    phone_number = Column(String(64), nullable=True)
    wechat_number = Column(String(64), nullable=True)
    major = Column(String(64), nullable=True)
    degree = Column(String(64), nullable=True)
    gender = Column(String(16), nullable=True)
    #
    owned_teams = relationship("Team", back_populates="captain")
    joined_teams = relationship("Team", secondary=TeamMember, back_populates="members", passive_deletes=True)
    applied_teams = relationship("Team", secondary=TeamApplication, back_populates="applicants", passive_deletes=True)
    #
    collections = relationship(
        "Competition", secondary=UserCollection, back_populates="collected_users", cascade="all, delete"
    )
