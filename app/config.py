from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()