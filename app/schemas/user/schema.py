from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    email: str
    password: str
    name: str


class CreateUserSchemaResponse(CreateUserSchema):
    id: int

    class Config:
        orm_mode = True
