from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Depends

from app.config.settings import Settings
from app.database.config import Base, engine
from app.routes.auth_router import auth_router

@lru_cache
def get_settings():
    return Settings()

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router=auth_router)
