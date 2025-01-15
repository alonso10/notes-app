from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database.models.user_model import UserModel
from app.schemas.user.schema import CreateUserSchema


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: CreateUserSchema):
        hashed_password = self.__password_hash(user.password)
        model = UserModel(name=user.name, email=user.email, password=hashed_password)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def __password_hash(self, password: str):
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.hash(password)
