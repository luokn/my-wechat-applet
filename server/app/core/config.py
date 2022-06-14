from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE: str
    APP_ID: str
    APP_SECRET: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_DAYS: int
    TEST_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
