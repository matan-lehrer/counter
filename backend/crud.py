from sqlalchemy.orm import Session
from backend import models, schemas
from typing import List


def get_counters(db: Session, skip: int = 0, limit: int = 10) -> List[models.Counter]:
    return db.query(models.Counter).offset(skip).limit(limit).all()

def create_counter(db: Session, counter: schemas.CounterCreate) -> models.Counter:
    db_counter = models.Counter(
        current_number=counter.current_number,
        previous_number=counter.previous_number,
        function_used=counter.function_used
    )
    db.add(db_counter)
    db.commit()
    db.refresh(db_counter)
    return db_counter

# increase / decrease / insert the current counter
def increase_counter(db: Session) -> models.Counter:
    previous_db_count = _get_latest_count(db)
    if not previous_db_count:
        raise ValueError("No count found in database.")
    new_counter = schemas.CounterCreate(
        current_number=previous_db_count.current_number + 1,
        previous_number=previous_db_count.current_number,
        function_used="increase 1"
    )
    return create_counter(db, new_counter)

def decrease_counter(db: Session) -> models.Counter:
    previous_db_count = _get_latest_count(db)
    if not previous_db_count:
        raise ValueError("No count found in database.")
    new_counter = schemas.CounterCreate(
        current_number=previous_db_count.current_number - 1,
        previous_number=previous_db_count.current_number,
        function_used="decrease 1"
    )
    return create_counter(db, new_counter)

def insert_counter(db: Session, new_number: int) -> models.Counter:
    previous_db_count = _get_latest_count(db)
    if not previous_db_count:
        raise ValueError("No count found in database.")
    new_counter = schemas.CounterCreate(
        current_number=new_number,
        previous_number=previous_db_count.current_number,
        function_used="insert"
    )
    return create_counter(db, new_counter)

def _get_latest_count(db: Session) -> models.Counter:
    return db.query(models.Counter).order_by(models.Counter.id.desc()).first()
