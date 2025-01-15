from functools import lru_cache
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.config.settings import Settings
from app.database.config import Base, engine
from app.routes.auth_router import auth_router
from app.services.errors import GeneralException, ApiErrorMessage, UserAlreadyExistsException


@lru_cache
def get_settings():
    return Settings()


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router=auth_router, prefix="/api")

@app.exception_handler(GeneralException)
async def general_exception_handler(request: Request, exc: GeneralException):
    error = ApiErrorMessage(type=exc.__class__.__name__, message=str(exc.message), status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return JSONResponse(status_code=error.status, content=error.dict())

@app.exception_handler(UserAlreadyExistsException)
async def general_exception_handler(request: Request, exc: UserAlreadyExistsException):
    error = ApiErrorMessage(type=exc.__class__.__name__, message=str(exc.message), status=exc.status)
    return JSONResponse(status_code=error.status, content=error.dict())
