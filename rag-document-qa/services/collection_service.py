from sqlalchemy.orm import Session
from ..models.collection import Collection
from ..schemas.collection import CollectionCreate

def create_collection(db: Session, collection: CollectionCreate) -> Collection:
    db_collection = Collection(
        name=collection.name,
        description=collection.description,
        document_count=0
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection

def get_collections(db: Session):
    total = db.query(Collection).count()
    collections = db.query(Collection).all()
    return collections, total

def delete_collection_by_id(db: Session, collection_id: str):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        return None
    
    # Store name for response before deleting
    name = collection.name
    doc_count = collection.document_count
    
    db.delete(collection)
    db.commit()
    
    return {
        "name": name,
        "deleted_documents": doc_count,
        "deleted_chunks": doc_count * 10  # Placeholder for chunks
    }
