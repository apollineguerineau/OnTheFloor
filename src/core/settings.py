from typing import Optional
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_db: str = "db"
    postgres_host: str = "host"
    postgres_port: int = 5432

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def database_url(self) -> str:
        print(f"URL : postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()


