from fastapi import FastAPI, APIRouter, Request
from project.db import database
from project.db.base import Base
from project.auth.jwt import router_auth
from project.controllers.controllers import router_customer_management
from project.controllers.controllers import router_payment_management
from project.services.asaas.payment_generator import test_route
from project.log_config import logger
from starlette.middleware.base import BaseHTTPMiddleware
from project.middleware import log_requests_middleware


Base.metadata.create_all(bind=database.engine)
logger.info("Database tables created")

app = FastAPI()
# an alternative way for setting a middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests_middleware)

logger.info("Starting API")
api_version_router = APIRouter(
    prefix="/api/v1"
)
api_version_router.include_router(router_auth)
api_version_router.include_router(router_customer_management)
api_version_router.include_router(router_payment_management)
app.include_router(api_version_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
