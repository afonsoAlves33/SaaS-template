from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from project.db import database
from project.models import user as models
from project.db.base import Base
from project.auth.routes import router
from project.auth.jwt import router_auth

app = FastAPI()
app.include_router(router)
app.include_router(router_auth)

Base.metadata.create_all(bind=database.engine)

@app.get("/users/")
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.UserModel).all()
    return users
