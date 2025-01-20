from fastapi import APIRouter
from fastapi.params import Depends

from app.config.bootstrap import init_user_service, init_login_service
from app.schemas.user.schema import (
    CreateUserSchema,
    CreateUserSchemaResponse,
    UserLoginSchema,
    UserLoginSchemaResponse,
)
from app.services.user.login_service import UserLoginService
from app.services.user.service import UserService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=CreateUserSchemaResponse)
async def register(
    user_request: CreateUserSchema,
    user_service: UserService = Depends(init_user_service),
):
    return await user_service.create_user(user_request)


@auth_router.post("/login", response_model=UserLoginSchemaResponse)
async def login(
    request: UserLoginSchema,
    login_service: UserLoginService = Depends(init_login_service),
):
    return await login_service.execute(request.email, request.password)
