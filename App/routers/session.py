from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/sessions", tags=["sessions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route sécurisée : ajout d'une séance
@router.post("/", response_model=schemas.SessionOut)
def create_new_session(
    session_data: schemas.SessionBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_session(db, session_data)

# Route publique : lecture de toutes les séances
@router.get("/", response_model=List[schemas.SessionOut])
def get_session(db: Session = Depends(get_db)):
    return crud.get_sessions(db)
