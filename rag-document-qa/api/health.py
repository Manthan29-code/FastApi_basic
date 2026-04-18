from fastapi import APIRouter, Depends
from ..dependencies import get_vector_store, get_settings
from ..config import Settings
from ..schemas.health import HealthResponse
from langchain_chroma import Chroma


routes = APIRouter()

@routes.get("/health", response_model=HealthResponse)
def health(
    settings: Settings = Depends(get_settings),
    vector_store: Chroma = Depends(get_vector_store)
):
    client = vector_store._get_client()
    collections = client.list_collections()
    
    total_docs = 0
    for coll_name in [c.name for c in collections]:
        total_docs += client.get_collection(name=coll_name).count()

    return {
        "status": "healthy",
        "service": "rag-document-qa",
        "model": settings.MODEL_NAME,
        "embedding_model": settings.EMBEDDING_MODEL,
        "vector_store": "chromadb",
        "total_collections": len(collections),
        "total_documents_indexed": total_docs
    }
