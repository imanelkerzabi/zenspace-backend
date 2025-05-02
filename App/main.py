from fastapi import FastAPI
from App.database import engine, Base

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ZenSpace API works"}
