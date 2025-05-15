from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "abc123456def789ghi"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///../db/test.db"

    class Config:
        env_file = ".env"


settings = Settings()
