import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def generate_uuid():
    return f"col_{uuid.uuid4().hex[:8]}"

class Collection(Base):
    __tablename__ = "collections"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    document_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    documents = relationship("Document", back_populates="collection", cascade="all, delete-orphan")