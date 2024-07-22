from pydantic import BaseModel
from datetime import datetime

class CounterBase(BaseModel):
    current_number: int
    previous_number: int
    function_used: str

class CounterCreate(CounterBase):
    pass

class Counter(CounterBase):
    id: int
    time_stamp: datetime

    class Config:
        from_attributes = True
