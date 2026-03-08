from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class SummaryLength(str, Enum):
    short = "short"
    medium = "medium"
    detailed = "detailed"

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="The text to synthesize")
    length: SummaryLength = Field(default=SummaryLength.medium, description="The length type of the summary")
    temperature: Optional[float] = Field(default=0.3, ge=0.0, le=1.0)

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float