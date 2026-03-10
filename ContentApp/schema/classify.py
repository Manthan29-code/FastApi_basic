from pydantic import BaseModel, Field
from typing import Optional


# Request Body
# {
#   "text": "The stock market rallied today as tech shares surged 5%...",
#   "categories": ["technology", "finance", "sports", "politics", "entertainment"],
#   "multi_label": false          // optional — allow multiple labels?
# }

# Response (200)
# {
#   "text_preview": "The stock market rallied today...",
#   "predicted_category": "finance",
#   "confidence": 0.89,
#   "all_scores": {
#     "finance": 0.89,
#     "technology": 0.45,
#     "politics": 0.12,
#     "sports": 0.03,
#     "entertainment": 0.01
#   }
# }

class classifyRequest(BaseModel):
    text: str = Field(..., description="Text to classify")
    categories: list[str] = Field(..., description="List of categories to classify into")
    multi_label: bool = Field(False, description="If true, allow multiple labels")


class classifyResponse(BaseModel):
    text_preview: str = Field(..., description="Preview of the input text")
    predicted_category: str = Field(..., description="The top predicted category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the predicted category")
    all_scores: dict[str, float] = Field(..., description="Confidence scores for all categories")
