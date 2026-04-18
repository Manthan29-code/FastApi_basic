from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    service: str
    model: str
    embedding_model: str
    vector_store: str
    total_collections: int
    total_documents_indexed: int
