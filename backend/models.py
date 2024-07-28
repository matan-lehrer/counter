from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Counter(Base):
    __tablename__ = "counter"

    id = Column(Integer, primary_key=True, index=True)
    current_count = Column(Integer, index=True)
    session_id = Column(String, ForeignKey("session.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    session = relationship("Session", back_populates="counters")

class Session(Base):
    __tablename__ = "session"

    id = Column(String, primary_key=True, index=True)

    counters = relationship("Counter", back_populates="session")
