from typing import Annotated, Any

from fastapi.params import Depends

from app.database.config import get_db
from app.services.user.service import UserService


def user_service(db: Annotated[Any, Depends(get_db)]) -> UserService:
    return UserService(db=db)
