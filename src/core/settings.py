from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_db: str = "db"
    postgres_host: str = "host"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()


