from pydantic import BaseModel
from datetime import datetime
from typing import List

class CounterBase(BaseModel):
    current_count: int

class CounterCreate(CounterBase):
    pass

class Counter(CounterBase):
    id: int
    session_id: int 
    time_stamp: datetime

    class Config:
        orm_mode = True

class Session(BaseModel):
    id: int
    counters: List[Counter] = []

    class Config:
        orm_mode = True
