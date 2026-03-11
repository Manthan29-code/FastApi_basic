from pydantic import BaseModel, Field
from typing import Optional


# Request Body
# {
#   "text": "Hey, so basically the server crashed and we lost some data lol",
#   "tone": "formal",             // "formal" | "casual" | "technical" | "simplified" | "persuasive"
#   "preserve_meaning": true      // optional, default true
# }

# Response (200)
# {
#   "original": "Hey, so basically the server crashed and we lost some data lol",
#   "rewritten": "We experienced an unexpected server failure that resulted in partial data loss.",
#   "tone_applied": "formal",
#   "changes_made": [
#     "Removed informal language",
#     "Restructured for professional tone",
#     "Clarified the impact statement"
#   ]
# }


class RewriteRequest(BaseModel):
    text: str = Field(..., description="The text to rewrite")
    tone: str = Field(..., description="Target tone: formal, casual, technical, simplified, or persuasive")
    preserve_meaning: bool = Field(True, description="Whether to preserve the original meaning")


class RewriteResponse(BaseModel):
    original: str = Field(..., description="The original input text")
    rewritten: str = Field(..., description="The rewritten text in the requested tone")
    tone_applied: str = Field(..., description="The tone that was applied")
    changes_made: list[str] = Field(..., description="List of changes made during rewriting")
