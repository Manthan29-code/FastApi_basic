from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.collection import CollectionCreate, CollectionResponse
from ..services.collection_service import create_collection, get_collections, delete_collection_by_id
from ..db.session import get_db

router = APIRouter(
    prefix="/api/v1/collections",
    tags=["Collections"]
)

@router.post(
    "", 
    response_model=CollectionResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new document collection",
    description="Create a named document collection (like a folder/namespace for docs)"
)
def create_new_collection(collection: CollectionCreate, db: Session = Depends(get_db)):
    return create_collection(db=db, collection=collection)

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List all document collections",
    description="List all document collections"
)
def list_collections(db: Session = Depends(get_db)):
    collections, total = get_collections(db)
    return {
        "collections": collections,
        "total": total
    }

@router.delete(
    "/:collection_id",
    status_code=status.HTTP_200_OK,
    summary="Delete a collection",
    description="Delete a collection and all its documents/embeddings"
)
def delete_collection(collection_id: str, db: Session = Depends(get_db)):
    result = delete_collection_by_id(db, collection_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found for " + collection_id)
        
    return {
        "message": f"Collection '{result['name']}' and all its documents have been deleted",
        "deleted_documents": result["deleted_documents"],
        "deleted_chunks": result["deleted_chunks"]
    }
