from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    class Config:
        env_file = ".env" #docker setting
        #env_file = "../.env" #local setting

settings = Settings()
# gebruik settings.DB_HOST etc.