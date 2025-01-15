from typing import Annotated, Any

from fastapi.params import Depends

from app.config.settings import settings
from app.database.config import get_db
from app.services.hash.password import HashPasswordService
from app.services.jwt.service import JWTService
from app.services.user.login_service import UserLoginService
from app.services.user.service import UserService


def init_user_service(db: Annotated[Any, Depends(get_db)]) -> UserService:
    return UserService(db=db, hash_service=HashPasswordService())

def init_login_service(db: Annotated[Any, Depends(get_db)]) -> UserLoginService:
    user_service = init_user_service(db)
    return UserLoginService(user_service=user_service, jwt_service=JWTService(settings=settings))