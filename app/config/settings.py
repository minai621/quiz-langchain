# app/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    langsmith_api_key: str = None  # 필요 시
    aws_access_key_id: str = None    # 필요 시
    aws_secret_access_key: str = None  # 필요 시

    class Config:
        env_file = ".env"

settings = Settings()
