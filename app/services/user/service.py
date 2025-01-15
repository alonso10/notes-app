from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database.models.user_model import UserModel
from app.schemas.user.schema import CreateUserSchema
from app.services.errors import UserAlreadyExistsException


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def __password_hash(self, password: str):
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.hash(password)

    def create_user(self, user: CreateUserSchema):
        user_by_email = self.get_user_by_email(user.email)

        if user_by_email:
            raise UserAlreadyExistsException(user.email)

        hashed_password = self.__password_hash(user.password)
        model = UserModel(name=user.name, email=user.email, password=hashed_password)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()
