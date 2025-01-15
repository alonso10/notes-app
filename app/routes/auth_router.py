from fastapi import APIRouter
from fastapi.params import Depends

from app.config.bootstrap import user_service
from app.schemas.user.schema import CreateUserSchema, CreateUserSchemaResponse
from app.services.user.service import UserService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=CreateUserSchemaResponse)
async def register(
    userRequest: CreateUserSchema, userService: UserService = Depends(user_service)
):
    return userService.create_user(userRequest)
