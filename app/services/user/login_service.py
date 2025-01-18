from app.schemas.user.schema import UserLoginSchemaResponse, UserDataScheme, UserAuthSchema
from app.services.errors import CredentialsException
from app.services.jwt.service import JWTService
from app.services.user.service import UserService


class UserLoginService:
    def __init__(self, user_service: UserService, jwt_service: JWTService):
        self.userService = user_service
        self.jwtService = jwt_service

    def execute(self, email: str, password: str):
        user = self.userService.get_user_by_email(email)
        if user and self.userService.hashService.verify_password(
            password, user.password
        ):
            token = self.jwtService.create_access_token({"sub": user.email})
            user_schema = UserDataScheme(id=user.id, email=user.email, name=user.name)
            auth_schema = UserAuthSchema(token=token)
            return UserLoginSchemaResponse(user=user_schema, auth=auth_schema)
        raise CredentialsException()
