from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from project.db import database
from project.models import user as models
from project.db.base import Base
from project.auth.jwt import router_auth

# create database data
Base.metadata.create_all(bind=database.engine)

app = FastAPI()
api_version_router = APIRouter(
    prefix="/api/v1"
)
api_version_router.include_router(router_auth)
app.include_router(api_version_router)
