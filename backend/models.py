from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class Counter(Base):
    __tablename__ = "counter_log"

    id = Column(Integer, primary_key=True, index=True)
    current_number = Column(Integer, index=True)
    previous_number = Column(Integer)
    function_used = Column(String)
    time_stamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
