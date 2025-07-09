from pydantic_settings import BaseSettings
from datetime import timedelta
import os

ENV = os.getenv('ENV', 'dev')

class Settings(BaseSettings):
    SECRET_KEY: str = "super-secret-key"
    OPENAI_API_KEY: str = "super-expensive-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"  # for local dev

    @property
    def access_token_expires(self):
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def refresh_token_expires(self):
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)

    class Config:
        env_file = f".env.{ENV}"
        env_file_encoding = "utf-8"

settings = Settings()