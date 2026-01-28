from pydantic_settings import BaseSettings
from os import getenv

class Settings(BaseSettings):
    DB_HOST: str = getenv("DB_HOST", "localhost")
    DB_PORT: int = int(getenv("DB_PORT", 5432))
    DB_USER: str = getenv("DB_USER", "user")
    DB_PASS: str = getenv("DB_PASS", "password")
    DB_NAME: str = getenv("DB_NAME", "database")
    DB_POOL_SIZE: int = int(getenv("DB_POOL_SIZE", 10))
    DB_MAX_OVERFLOW: int = int(getenv("DB_MAX_OVERFLOW", 20))
    DB_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
settings = Settings()
# gebruik settings.DB_HOST etc.