from contextlib import asynccontextmanager
from functools import lru_cache
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.config.settings import Settings
from app.database.config import init_models, sessionmanager
from app.routes.auth_router import auth_router
from app.routes.notes_router import notes_router
from app.services.errors import (
    GeneralException,
    ApiErrorMessage,
)


@lru_cache
def get_settings():
    return Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init(get_settings().get_database_url())
    async with sessionmanager.connect() as connection:
        await init_models(connection)
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router=auth_router, prefix="/api")
app.include_router(router=notes_router, prefix="/api")


@app.exception_handler(GeneralException)
async def general_exception_handler(request: Request, exc: GeneralException):
    error = ApiErrorMessage(
        type=exc.__class__.__name__,
        message=str(exc.message),
        status=exc.status if exc.status else HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    return JSONResponse(status_code=error.status, content=error.model_dump())
