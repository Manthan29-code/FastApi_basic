from pydantic import BaseModel, Field
from typing import Optional


# Request Body
# {
#   "text": "Elon Musk announced that Tesla will open a new Gigafactory in Texas...",
#   "max_keywords": 10            // optional, default 10
# }

# Response (200)
# {
#   "keywords": ["Tesla", "Gigafactory", "Texas", "electric vehicles", "manufacturing"],
#   "entities": [
#     { "text": "Elon Musk", "type": "PERSON" },
#     { "text": "Tesla", "type": "ORGANIZATION" },
#     { "text": "Texas", "type": "LOCATION" }
#   ],
#   "topics": ["automotive", "manufacturing", "business expansion"]
# }


class keywordRequest(BaseModel):
    text: str = Field(..., description="Text to extract keywords and entities from")
    max_keywords: int = Field(10, description="Maximum number of keywords to return")


class Entity(BaseModel):
    text: str = Field(..., description="The entity text")
    type: str = Field(..., description="Entity type, e.g. PERSON, ORGANIZATION, LOCATION")


class keywordResponse(BaseModel):
    keywords: list[str] = Field(..., description="List of extracted key phrases")
    entities: list[Entity] = Field(..., description="List of named entities with their types")
    topics: list[str] = Field(..., description="List of identified topics")