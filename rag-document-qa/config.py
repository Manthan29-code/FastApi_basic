# BaseSettings — API keys, chunk sizes, model names
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    CHROMA_PERSIST_DIR: str = "./rag-document-qa/storage/chroma_db"
    UPLOAD_DIR: str = "./rag-document-qa/storage/uploads"
    DATABASE_URL: str = "sqlite:///./rag-document-qa/storage/metadata.db"


    class Config:
        env_file = ".env"
        extra = "allow"


  


