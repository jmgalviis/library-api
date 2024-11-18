from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:admin123@localhost:5432/library"

    class Config:
        env_file = ".env"


settings = Settings()
