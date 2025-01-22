from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models.user_model import UserModel
from app.schemas.user.schema import CreateUserSchema
from app.services.errors import UserAlreadyExistsException
from app.services.hash.password import HashPasswordService


class UserService:
    def __init__(self, db: AsyncSession, hash_service: HashPasswordService):
        self.hashService = hash_service
        self.db = db

    async def create_user(self, user: CreateUserSchema):
        user_by_email = await self.get_user_by_email(user.email)

        if user_by_email:
            raise UserAlreadyExistsException(user.email)

        hashed_password = self.hashService.hash_password(user.password)
        model = UserModel(
            name=user.name, email=user.email, password=hashed_password
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(UserModel).filter_by(email=email))
        user = result.scalars().first()
        if user is None:
            return None
        return user
