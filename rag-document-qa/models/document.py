import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .collection import Base


def generate_document_uuid() -> str:
    return f"doc_{uuid.uuid4().hex[:8]}"


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_document_uuid, index=True)
    collection_id = Column(String, ForeignKey("collections.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    status = Column(String, default="processing", nullable=False)
    chunks_created = Column(Integer, default=0, nullable=False)
    total_characters = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    collection = relationship("Collection", back_populates="documents")
