from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"
    DEFAULT_TEMPERATURE: float = 0.3
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        extra = "allow"
