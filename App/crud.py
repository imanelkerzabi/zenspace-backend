#from warnings import deprecated
from ast import mod
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.routers import progress

from . import models, schemas 

#Création d'un contexte pour hasher les mots de passe 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#Clé secréte pour les tokens JWT 
SECRET_KEY = "verysecretkey"
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Fonction pour hasher un mot de passe 
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Fonction pour créer un nouvel utilisateur
def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Fonction pour retrouver un utilisateur par son email 
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


#Fonction pour vérifier le mot de passe 
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#Fonction pour authentifier un utilisateur 
def authenticate_user(db: Session, email: str, password: str):
  user = get_user_by_email(db, email)
  if not user:
      return None
  if not verify_password(password, user.hashed_password):
      return None
  return user

#Créer un token JWT pour l'utilisateur connecté 
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def create_session(db: Session, session_data: schemas.SessionBase):
    db_session = models.Session(**session_data.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


# Récupérer toutes les séances de méditation
def get_sessions(db: Session):
    return db.query(models.Session).all()


def create_progress(db: Session, user_id: int, session_id: int):
    new_progress = models.Progress(
        user_id = user_id,
        session_id = session_id,
        started_at=datetime.utcnow()
    )
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return new_progress

def get_my_progress(db: Session, user_id: int):
    return db.query(models.Progress).filter(models.Progress.user_id == user_id).all()

def complete_progess(db: Session, progress_id: int, user_id: int):
    progress = db.query(models.Progress).filter(
        models.Progress.id == progress_id,
        models.Progress.user_id == user_id
    ).first()

    if not progress:
        return None
    
    progress.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(progress)
    return progress


def get_user_statistics(db: Session, user_id: int):
    total_started = db.query(models.Progress).filter(models.Progress.user_id == user_id).count()
    total_completed = db.query(models.Progress).filter(
        models.Progress.user_id == user_id,
        models.Progress.completed_at != None
    ).count()

    if total_started == 0:
        completion_rate = 0.0
    else:
        completion_rate = (total_completed / total_started) * 100

    return {
        "total_sessions_started": total_started,
        "total_sessions_completed": total_completed,
        "completion_rate": round(completion_rate, 2)
    }



