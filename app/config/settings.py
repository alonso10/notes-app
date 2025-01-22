from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    secret_key: str
    jwt_algorithms: str
    jwt_expiration: int

    model_config = SettingsConfigDict(env_file=".env")

    def get_database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
