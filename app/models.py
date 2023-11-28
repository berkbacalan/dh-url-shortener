from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime

from .database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    short_url = Column(String, index=True)
    clicks = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.utcnow())
    expiry_date = Column(DateTime, default=datetime.utcnow() + timedelta(days=30))
