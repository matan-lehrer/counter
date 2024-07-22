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
@router.get("/counter/", response_model=List[schemas.Counter])
def read_counters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        counters = crud.get_counters(db, skip=skip, limit=limit)
        return counters
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/counter/", response_model=schemas.Counter)
def create_counter(counter: schemas.CounterCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_counter(db=db, counter=counter)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Custom endpoints
@router.post("/counter/increase", response_model=schemas.Counter)
def increase_counter(db: Session = Depends(get_db)):
    try:
        return crud.increase_counter(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/counter/decrease", response_model=schemas.Counter)
def decrease_counter(db: Session = Depends(get_db)):
    try:
        return crud.decrease_counter(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/counter/insert", response_model=schemas.Counter)
def insert_counter(new_number: int, db: Session = Depends(get_db)):
    try:
        return crud.insert_counter(db=db, new_number=new_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
