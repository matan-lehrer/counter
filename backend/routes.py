from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import crud, schemas
from backend.database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# General endpoints
@router.get("/{session_id}/counter/", response_model=List[schemas.Counter])
def read_counters(session_id: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        counters = crud.get_counters(db, session_id=session_id, skip=skip, limit=limit)
        return counters
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{session_id}/counter/", response_model=schemas.Counter)
def create_counter(session_id: str, counter: schemas.CounterCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_counter(db=db, session_id=session_id, counter=counter)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{session_id}/", response_model=schemas.Session)
def delete_session(session_id: str, db: Session = Depends(get_db)):
    try:
        session = crud.delete_session(db=db, session_id=session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Custom endpoints
@router.post("/{session_id}/counter/increase", response_model=schemas.Counter)
def increase_counter(session_id: str, db: Session = Depends(get_db)):
    try:
        return crud.increase_counter(db=db, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{session_id}/counter/decrease", response_model=schemas.Counter)
def decrease_counter(session_id: str, db: Session = Depends(get_db)):
    try:
        return crud.decrease_counter(db=db, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{session_id}/counter/insert", response_model=schemas.Counter)
def insert_counter(session_id: str, new_number: int, db: Session = Depends(get_db)):
    try:
        return crud.insert_counter(db=db, new_number=new_number, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
