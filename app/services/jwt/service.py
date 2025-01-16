from datetime import datetime, timedelta, timezone

import jwt

from app.config.settings import Settings


class JWTService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_access_token(self, data: dict) -> str:
        data_to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.settings.jwt_expiration)
        data_to_encode.update({"exp": expire})
        return jwt.encode(data_to_encode, self.settings.secret_key, algorithm=self.settings.jwt_algorithms)

    def decode_token(self, token: str):
        return jwt.decode(token, self.settings.secret_key, algorithms=[self.settings.jwt_algorithms])
