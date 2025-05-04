from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# UTILISATEURS

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


#  SÉANCES DE MÉDITATION

class SessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration: Optional[int] = None
    audio_url: str
    category: str

class SessionOut(SessionBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

# PROGRESSION DE L'UTILISATEUR

class ProgressBase(BaseModel):
    session_id: int

class ProgressOut(ProgressBase):
    id: int
    user_id: int
    started_at: datetime
    completed_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
