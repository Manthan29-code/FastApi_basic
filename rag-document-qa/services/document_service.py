from sqlalchemy.orm import Session

from ..core.document_loader import load_document
from ..core.text_splitter import get_text_splitter
from ..db.session import SessionLocal
from ..dependencies import get_embeddings
from ..models.collection import Collection
from ..models.document import Document
from .vector_store_service import add_documents_to_store


def create_document_record(
	db: Session,
	*,
	collection_id: str,
	filename: str,
	file_size_bytes: int,
) -> Document:
	document = Document(
		collection_id=collection_id,
		filename=filename,
		file_size_bytes=file_size_bytes,
		status="processing",
		chunks_created=0,
		total_characters=0,
	)
	db.add(document)
	db.commit()
	db.refresh(document)
	return document


def list_documents_by_collection(db: Session, collection_id: str):
	return (
		db.query(Document)
		.filter(Document.collection_id == collection_id)
		.order_by(Document.created_at.desc())
		.all()
	)


def process_document_background(
	*,
	document_id: str,
	collection_id: str,
	file_path: str,
	chunk_size: int,
	chunk_overlap: int,
	persist_directory: str,
):
	db = SessionLocal()
	try:
		document = db.query(Document).filter(Document.id == document_id).first()
		if not document:
			return

		loaded_documents = load_document(file_path)
		splitter = get_text_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
		chunks = splitter.split_documents(loaded_documents)

		embeddings = get_embeddings()
		chunk_count = add_documents_to_store(
			chunks=chunks,
			embeddings=embeddings,
			persist_directory=persist_directory,
			collection_name=collection_id,
			document_id=document_id,
			filename=document.filename,
		)

		total_characters = sum(len(chunk.page_content) for chunk in chunks)
		document.status = "completed"
		document.chunks_created = chunk_count
		document.total_characters = total_characters

		collection = db.query(Collection).filter(Collection.id == collection_id).first()
		if collection:
			collection.document_count = db.query(Document).filter(Document.collection_id == collection_id).count()

		db.commit()
	except Exception:
		document = db.query(Document).filter(Document.id == document_id).first()
		if document:
			document.status = "failed"
			db.commit()
	finally:
		db.close()
