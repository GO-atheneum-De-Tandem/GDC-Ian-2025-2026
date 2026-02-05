from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
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
    DB_ECHO_QUERIES: bool = getenv("DB_ECHO_QUERIES", "true").lower() in ("true", "1", "yes")
    
    # JWT settings
    JWT_SECRET: str = getenv("JWT_SECRET", "change-this-secret")
    JWT_ALGORITHM: str = getenv("JWT_ALGORITHM", "HS256")
    JWT_EXP_MINUTES: int = int(getenv("JWT_EXP_MINUTES", 15))

    #Argon2 Hashing settings
    HASH_TIME_COST: int = int(getenv("HASH_TIME_COST", 3))
    HASH_MEMORY_COST: int = int(getenv("HASH_MEMORY_COST", 65536))  # in KB
    HASH_PARALLELISM: int = int(getenv("HASH_PARALLELISM", 4))
    HASH_SALT_LENGTH: int = int(getenv("HASH_SALT_LENGTH", 16))
    HASH_HASH_LENGTH: int = int(getenv("HASH_HASH_LENGTH", 32))
    
settings = Settings()
# gebruik settings.DB_HOST etc.

description = """
This is the **Safe API** for the GDC research project by Ian-Chains Baute.

This system is based on FastAPI and SQLAlchemy. It has features like posting blogposts, commenting, user authentication, and more.  
This version of the GDC API is safe, to provide **a secure environment** for educational purposes.  
This version has the extra features and steps implemented to **ensure security**.  
By looking at the differences between the safe and unsafe version, you can learn about **common security vulnerabilities** and how to mitigate them.  
Please use this API responsibly and **always** prioritize security in your applications.  
"""

#Base class voor models
Base = declarative_base()