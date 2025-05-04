from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.auth import get_current_user
from app.models import User
from typing import List

router = APIRouter(prefix="/progress", tags=["progress"])

# Accès à la DBB
def get_db():
  db = database.SessionLocal()
  try:
    yield db 
  finally:
    db.close()

# Route protégée pour enregistrer une progression
@router.post("/", response_model=schemas.ProgressOut)
def start_progress(
  progress_data: schemas.ProgressBase,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)

):
 return crud.create_progress(db, user_id=current_user.id, session_id=progress_data.session_id)

@router.get("/mine", response_model=List[schemas.ProgressOut])
def red_my_progress(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)

):
  return crud.get_my_progress(db, user_id=current_user.id)

@router.put("/{progress_id}/complete", response_model=schemas.ProgresOut)
def mark_session_complete(
  progress_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)

):
  
 progress = crud.complete_progess(db, progress_id, current_user.id)
 if not progress:
  raise HTTPException(status_code=404, details="Progression non trouvée ou non autorisée")
 return progress


@router.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_user_statistics(db, current_user.id)



