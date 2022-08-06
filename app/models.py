from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'betterposts'
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False)
    user_id = Column(Integer, ForeignKey("betterusers.id", ondelete="CASCADE"), nullable = False)
    user = relationship("User")

class User(Base):
    __tablename__ = 'betterusers'
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False)


class Vote(Base):
    __tablename__ = 'bettervotes'
    post_id = Column(Integer, ForeignKey("betterposts.id", ondelete="CASCADE"), primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("betterusers.id", ondelete="CASCADE"), primary_key = True, nullable = False)
    