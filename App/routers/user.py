from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models
from app.auth import get_current_user
from ..models import User as DBUser
from .. import crud, schemas, database

router = APIRouter(prefix="/users", tags=["users"])


# Obtenir la session de base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route d’inscription
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")
    return crud.create_user(db, user)

# Route de connexion (login)
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

#  Route protégée : retourne l'utilisateur connecté avec Security
@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: DBUser = Depends(get_current_user)):
    return current_user



