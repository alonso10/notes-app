from http import HTTPStatus

from pydantic import BaseModel


class GeneralException(Exception):
    def __init__(self, status: HTTPStatus, message: str):
        self.status = status
        self.message = message
        super().__init__(message)

class UserAlreadyExistsException(GeneralException):
    def __init__(self, email: str):
        super().__init__(HTTPStatus.CONFLICT, f"User with {email} already exists")


class ApiErrorMessage(BaseModel):
    message: str
    status: int
    type: str