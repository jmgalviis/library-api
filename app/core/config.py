from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/library_db"

    class Config:
        env_file = ".env"


settings = Settings()
