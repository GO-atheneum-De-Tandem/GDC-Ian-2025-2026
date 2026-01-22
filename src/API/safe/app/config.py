from pydantic_settings import BaseSettings
from os import getenv

class Settings(BaseSettings):
    DB_HOST: str = getenv("DB_HOST", "localhost")
    DB_PORT: int = int(getenv("DB_PORT", 5432))
    DB_USER: str = getenv("DB_USER", "user")
    DB_PASS: str = getenv("DB_PASS", "password")
    DB_NAME: str = getenv("DB_NAME", "database")
    
settings = Settings()
# gebruik settings.DB_HOST etc.