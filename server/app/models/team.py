from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .team_application import TeamApplication
from .team_member import TeamMember


class Team(Base):
    name = Column(String(256), nullable=False)
    captain_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    competition_id = Column(Integer, ForeignKey("competition.id", ondelete="SET NULL"), nullable=False)
    name_words = Column(String(256), nullable=False)
    introduce = Column(String(1024), nullable=False)
    requirements = Column(String(1024), nullable=False)
    deadline = Column(DateTime, nullable=False)
    #
    competition = relationship("Competition", uselist=False, back_populates="teams")
    captain = relationship("User", uselist=False, back_populates="owned_teams")
    members = relationship("User", secondary=TeamMember, back_populates="joined_teams", cascade="all, delete")
    applicants = relationship("User", secondary=TeamApplication, back_populates="applied_teams", cascade="all, delete")
