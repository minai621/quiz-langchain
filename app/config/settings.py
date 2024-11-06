from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    deepl_api_key: str
    langsmith_api_key: str = None
    aws_access_key_id: str = None
    aws_secret_access_key: str = None

    class Config:
        env_file = ".env"

settings = Settings()
