from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATA_PATH: str = "./data"
    PORT: int = 8888

    class Config:
        env_file = ".env"

settings = Settings()
