from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    email: str
    password: str
    name: str


class CreateUserSchemaResponse(CreateUserSchema):
    id: int

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserLoginSchemaResponse(BaseModel):
    token: str
    token_type: str = "bearer"
