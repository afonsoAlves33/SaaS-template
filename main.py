from fastapi import FastAPI, APIRouter
from project.db import database
from project.db.base import Base
from project.auth.jwt import router_auth
from services.asaas import router_tests

# create database data
Base.metadata.create_all(bind=database.engine)

app = FastAPI()
api_version_router = APIRouter(
    prefix="/api/v1"
)
api_version_router.include_router(router_auth)
api_version_router.include_router(router_tests)
app.include_router(api_version_router)
