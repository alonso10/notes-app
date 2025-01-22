from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    email: str
    password: str
    name: str


class CreateUserSchemaResponse(CreateUserSchema):
    id: int

    class ConfigDict:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserDataScheme(BaseModel):
    id: int
    email: str
    name: str

    class ConfigDict:
        from_attributes = True


class UserAuthSchema(BaseModel):
    token: str
    token_type: str = "bearer"


class UserLoginSchemaResponse(BaseModel):
    user: UserDataScheme
    auth: UserAuthSchema
