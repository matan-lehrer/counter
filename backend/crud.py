from sqlalchemy.orm import Session
from backend import models, schemas
from typing import List

def get_counters(db: Session, session_id: str, skip: int = 0, limit: int = 10) -> List[models.Counter]:
    return db.query(models.Counter).filter_by(session_id=session_id).offset(skip).limit(limit).all()

def create_counter(db: Session, session_id: str, counter: schemas.CounterCreate) -> models.Counter:
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

def delete_session(db: Session, session_id: str) -> models.Session:
    session = db.query(models.Session).filter_by(id=session_id).first()
    if session:
        db.query(models.Counter).filter_by(session_id=session_id).delete()
        db.delete(session)
        db.commit()
        return session
    return None

def increase_counter(db: Session, session_id: str) -> models.Counter:
    return _modify_counter(db, session_id, lambda count: count + 1, initial_value=1)

def decrease_counter(db: Session, session_id: str) -> models.Counter:
    return _modify_counter(db, session_id, lambda count: count - 1, initial_value=-1)

def insert_counter(db: Session, session_id: str, new_number: int) -> models.Counter:
    return create_counter(db, session_id, schemas.CounterCreate(current_count=new_number))

def _get_latest_count(db: Session, session_id: str) -> models.Counter:
    return db.query(models.Counter).filter_by(session_id=session_id).order_by(models.Counter.id.desc()).first()

def _modify_counter(db: Session, session_id: str, modify_func, initial_value: int) -> models.Counter:
    previous_db_count = _get_latest_count(db, session_id)
    if not previous_db_count:
        new_counter = schemas.CounterCreate(current_count=initial_value)
    else:
        new_counter = schemas.CounterCreate(current_count=modify_func(previous_db_count.current_count))
    return create_counter(db, session_id, new_counter)
