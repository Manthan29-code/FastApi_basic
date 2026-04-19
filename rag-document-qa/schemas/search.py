from typing import Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
	query: str = Field(..., min_length=1, description="Semantic search query")
	top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
	score_threshold: float = Field(default=0.4, ge=0.0, le=1.0, description="Minimum relevance score")


class SearchResult(BaseModel):
	chunk_text: str
	source_document: str
	page_number: Optional[int] = None
	relevance_score: float
	metadata: dict = Field(default_factory=dict)


class SearchResponse(BaseModel):
	results: list[SearchResult]
	total_results: int
	query: str
