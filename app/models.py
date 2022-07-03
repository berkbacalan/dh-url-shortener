from sqlalchemy import Column, Integer, String

from .database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    short_url = Column(String, index=True)
    clicks = Column(Integer, default=0)