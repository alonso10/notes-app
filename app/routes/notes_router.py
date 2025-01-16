from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config.bootstrap import init_auth_user_service
from app.services.user.auth_service import UserAuthService

notes_router = APIRouter(prefix="/notes", tags=["notes"])
security = HTTPBearer()

def auth_required(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_service: UserAuthService = Depends(init_auth_user_service),
):
    return user_service.authenticate(credentials.credentials)

