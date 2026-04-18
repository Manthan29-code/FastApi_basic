import os
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from ..config import Settings
from ..db.session import get_db
from ..dependencies import get_settings
from ..models.collection import Collection
from ..schemas.document import UploadResponse
from ..services.document_service import (
	create_document_record,
	list_documents_by_collection,
	process_document_background,
)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

router = APIRouter(
	prefix="/api/v1/collections",
	tags=["Documents"],
)


@router.post(
	"/{collection_id}/upload",
	response_model=UploadResponse,
	status_code=status.HTTP_202_ACCEPTED,
	summary="Upload a document",
	description="Upload a document, chunk it, generate embeddings, and store in ChromaDB",
)
async def upload_document(
	collection_id: str,
	background_tasks: BackgroundTasks,
	file: UploadFile = File(...),
	chunk_size: int = Query(default=1000, ge=100),
	chunk_overlap: int = Query(default=200, ge=0),
	db: Session = Depends(get_db),
	settings: Settings = Depends(get_settings),
):
	if chunk_overlap >= chunk_size:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="chunk_overlap must be less than chunk_size")

	collection = db.query(Collection).filter(Collection.id == collection_id).first()
	if not collection:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Collection not found for {collection_id}")

	extension = Path(file.filename or "").suffix.lower()
	if extension not in SUPPORTED_EXTENSIONS:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Unsupported file format. Supported formats: .pdf, .txt, .md",
		)

	os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
	safe_name = f"{uuid.uuid4()}_{file.filename}"
	saved_path = os.path.join(settings.UPLOAD_DIR, safe_name)

	content = await file.read()
	with open(saved_path, "wb") as handle:
		handle.write(content)

	document = create_document_record(
		db,
		collection_id=collection_id,
		filename=file.filename or safe_name,
		file_size_bytes=len(content),
	)

	background_tasks.add_task(
		process_document_background,
		document_id=document.id,
		collection_id=collection_id,
		file_path=saved_path,
		chunk_size=chunk_size,
		chunk_overlap=chunk_overlap,
		persist_directory=settings.CHROMA_PERSIST_DIR,
	)

	return {
		"message": "Document uploaded and processing started",
		"document": document,
		"collection_id": collection_id,
	}


@router.get(
	"/{collection_id}/documents",
	status_code=status.HTTP_200_OK,
	summary="List documents in a collection",
	description="List all uploaded documents and processing status in a collection",
)
def list_documents(collection_id: str, db: Session = Depends(get_db)):
	collection = db.query(Collection).filter(Collection.id == collection_id).first()
	if not collection:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Collection not found for {collection_id}")

	documents = list_documents_by_collection(db, collection_id)
	return {
		"collection_id": collection_id,
		"documents": documents,
		"total": len(documents),
	}
