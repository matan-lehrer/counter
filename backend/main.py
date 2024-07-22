from fastapi import FastAPI
from backend import models
from backend.database import engine, SessionLocal
from backend.routes import router as counters_router
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(counters_router, prefix="/api")

# Initialize database with first counter
def initialize_db():
    db: Session = SessionLocal()
    try:
        if db.query(models.Counter).count() == 0:
            initial_counter = models.Counter(
                current_number=0,
                previous_number=0,
                function_used="Initial"
            )
            db.add(initial_counter)
            db.commit()
            db.refresh(initial_counter)
    finally:
        db.close()

initialize_db()
