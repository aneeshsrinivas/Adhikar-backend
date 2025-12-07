from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str | None = None
    gemini_api_url: str | None = None
    gemini_model: str = "gemini-1.5"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
