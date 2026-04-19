from typing import Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
	question: str = Field(..., min_length=1, description="Question to ask against collection documents")
	top_k: int = Field(default=4, ge=1, le=20, description="Number of chunks to retrieve")
	score_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum relevance score")
	include_sources: bool = Field(default=True, description="Whether to include source chunks")


class SourceChunk(BaseModel):
	chunk_text: str
	source_document: str
	page_number: Optional[int] = None
	relevance_score: float


class QueryResponse(BaseModel):
	answer: str
	confidence: str
	sources: list[SourceChunk] = Field(default_factory=list)
	chunks_retrieved: int
	chunks_used: int
