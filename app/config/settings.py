from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    jwt_algorithms: str
    jwt_expiration: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
