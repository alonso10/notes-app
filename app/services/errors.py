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


class CredentialsException(GeneralException):
    def __init__(self):
        super().__init__(HTTPStatus.UNAUTHORIZED, "Invalid credentials")


class TokenException(GeneralException):
    def __init__(self):
        super().__init__(HTTPStatus.UNAUTHORIZED, "Invalid token")


class NoteNotFoundException(GeneralException):
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, "Note not found")


class NoteUpdateBlockedException(GeneralException):
    def __init__(self):
        super().__init__(HTTPStatus.CONFLICT, "Note update blocked")


class ApiErrorMessage(BaseModel):
    message: str
    status: int
    type: str
