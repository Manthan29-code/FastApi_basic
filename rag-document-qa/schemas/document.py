from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
	id: str
	filename: str
	file_size_bytes: int
	status: str
	chunks_created: int
	total_characters: int
	created_at: datetime

	class Config:
		from_attributes = True


class UploadResponse(BaseModel):
	message: str
	document: DocumentResponse
	collection_id: str
