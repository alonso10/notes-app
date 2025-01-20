import jwt

from app.services.errors import TokenException
from app.services.user.service import UserService
from app.services.jwt.service import JWTService


class UserAuthService:
    def __init__(self, user_service: UserService, jwt_service: JWTService):
        self.userService = user_service
        self.jwtService = jwt_service

    async def authenticate(self, token: str):
        try:
            data = self.jwtService.decode_token(token)
            email: str = data.get("sub")
            if email is None:
                raise TokenException()
        except jwt.InvalidTokenError:
            raise TokenException()

        user = await self.userService.get_user_by_email(email)
        print("user", user)
        if user is None:
            raise TokenException()
        return user
