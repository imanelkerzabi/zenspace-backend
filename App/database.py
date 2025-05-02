from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 
from dotenv import load_dotenv
import os 


load_dotenv()   #Pour lire le fichier .env
DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(DATABASE_URL)  # (engine) Permet à SQLAlchemy de communiquer avec la BDD 

#une session DB utilisable dans tes routes 
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base() # sert à créer les modéles ORM (table)


