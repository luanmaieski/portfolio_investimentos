from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = "*"  # valor padrão se não tiver no .env

    class Config:
        env_file = ".env"

settings = Settings()
