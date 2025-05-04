from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import database, models

#  Clé secrète et algo JWT
SECRET_KEY = "verysecretkey"
ALGORITHM = "HS256"

#  Ce schéma permet à Swagger d'ajouter le bouton Authorize automatiquement
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Connexion DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Fonction pour décoder le token et retourner l'utilisateur courant
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou manquant",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 🔓 Décodage du token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 🔎 Recherche de l’utilisateur en base
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    return user
