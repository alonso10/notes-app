from sqlalchemy.orm import Session

from app.database.models.user_model import UserModel
from app.schemas.user.schema import CreateUserSchema
from app.services.errors import UserAlreadyExistsException
from app.services.hash.password import HashPasswordService


class UserService:
    def __init__(self, db: Session, hash_service: HashPasswordService):
        self.hashService = hash_service
        self.db = db

    def create_user(self, user: CreateUserSchema):
        user_by_email = self.get_user_by_email(user.email)

        if user_by_email:
            raise UserAlreadyExistsException(user.email)

        hashed_password = self.hashService.hash_password(user.password)
        model = UserModel(name=user.name, email=user.email, password=hashed_password)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()
