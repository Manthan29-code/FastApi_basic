from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..dependencies import get_embeddings, get_llm
from ..models.collection import Collection
from ..models.document import Document
from ..schemas.query import QueryRequest, QueryResponse
from ..schemas.search import SearchRequest, SearchResponse
from ..services.rag_service import query_documents, semantic_search

router = APIRouter(prefix="/api/v1", tags=["query"])


def _ensure_collection_exists(db: Session, collection_id: str) -> Collection:
	collection = db.query(Collection).filter(Collection.id == collection_id).first()
	if not collection:
		raise HTTPException(status_code=404, detail="Collection not found")
	return collection


def _ensure_collection_has_documents(db: Session, collection_id: str) -> None:
	count = db.query(Document).filter(Document.collection_id == collection_id).count()
	if count == 0:
		raise HTTPException(
			status_code=404,
			detail="No documents found in this collection. Upload a document first.",
		)


@router.post("/collections/{collection_id}/query", response_model=QueryResponse)
async def query_collection(
	collection_id: str,
	request: QueryRequest,
	db: Session = Depends(get_db),
	llm=Depends(get_llm),
	embeddings=Depends(get_embeddings),
):
	_ensure_collection_exists(db=db, collection_id=collection_id)
	_ensure_collection_has_documents(db=db, collection_id=collection_id)

	try:
		result = await query_documents(
			collection_id=collection_id,
			question=request.question,
			llm=llm,
			embeddings=embeddings,
			top_k=request.top_k,
			score_threshold=request.score_threshold,
			include_sources=request.include_sources,
		)
		return QueryResponse(**result)
	except HTTPException:
		raise
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Failed to run query: {str(exc)}") from exc


@router.post("/collections/{collection_id}/search", response_model=SearchResponse)
async def search_collection(
	collection_id: str,
	request: SearchRequest,
	db: Session = Depends(get_db),
	embeddings=Depends(get_embeddings),
):
	_ensure_collection_exists(db=db, collection_id=collection_id)
	_ensure_collection_has_documents(db=db, collection_id=collection_id)

	try:
		results = semantic_search(
			collection_id=collection_id,
			query=request.query,
			embeddings=embeddings,
			top_k=request.top_k,
			score_threshold=request.score_threshold,
		)
		return SearchResponse(results=results, total_results=len(results), query=request.query)
	except HTTPException:
		raise
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Failed to run semantic search: {str(exc)}") from exc
