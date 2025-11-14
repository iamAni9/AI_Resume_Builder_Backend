from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FRONTEND_ORIGIN: str
    ENV: str = "development"
    ENV_PORT: int = 10000
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()