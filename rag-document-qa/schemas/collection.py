from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class CollectionCreate(BaseModel):
    name: str = Field(..., description="Name of the collection", examples=["product-docs"])
    description: Optional[str] = Field(None, description="Description of the collection", examples=["Product documentation and user guides"])

class CollectionResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    document_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
