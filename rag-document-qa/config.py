# BaseSettings — API keys, chunk sizes, model names
from pydantic_settings import BaseSettings
from pydantic.v1 import BaseSettings
class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "models/embedding-001"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    CHROMA_PERSIST_DIR: str = "./app/storage/chroma_db"
    UPLOAD_DIR: str = "./app/storage/uploads"
    DATABASE_URL: str = "sqlite:///./app/storage/metadata.db"

    class Config:
        env_file = ".env"
        extra = "allow"


  


