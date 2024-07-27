from sqlalchemy.orm import Session
from backend import models, schemas
from typing import List

def get_counters(db: Session, session_id: int, skip: int = 0, limit: int = 10) -> List[models.Counter]:
    return db.query(models.Counter).filter_by(session_id=session_id).offset(skip).limit(limit).all()

def create_counter(db: Session, session_id: int, counter: schemas.CounterCreate) -> models.Counter:
    existing_session = db.query(models.Session).filter_by(id=session_id).first()

    if not existing_session:
        new_session = models.Session(id=session_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    db_counter = models.Counter(
        current_count=counter.current_count,
        session_id=session_id,
    )
    db.add(db_counter)
    db.commit()
    db.refresh(db_counter)
    return db_counter

def increase_counter(db: Session, session_id: int) -> models.Counter:
    previous_db_count = _get_latest_count(db, session_id)
    if not previous_db_count:
        raise ValueError("No count found in database.")
    new_counter = schemas.CounterCreate(
        current_count=previous_db_count.current_count + 1,
        session_id=session_id
    )
    return create_counter(db, session_id, new_counter)

def decrease_counter(db: Session, session_id: int) -> models.Counter:
    previous_db_count = _get_latest_count(db, session_id)
    if not previous_db_count:
        raise ValueError("No count found in database.")
    new_counter = schemas.CounterCreate(
        current_count=previous_db_count.current_count - 1,
        session_id=session_id
    )
    return create_counter(db, session_id, new_counter)

def insert_counter(db: Session, session_id: int, new_number: int) -> models.Counter:
    new_counter = schemas.CounterCreate(
        current_count=new_number,
        session_id=session_id
    )
    return create_counter(db, session_id, new_counter)

def _get_latest_count(db: Session, session_id: int) -> models.Counter:
    return db.query(models.Counter).filter_by(session_id=session_id).order_by(models.Counter.id.desc()).first()
