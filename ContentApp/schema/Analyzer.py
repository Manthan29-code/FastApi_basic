from pydantic import BaseModel, Field
from enum import Enum



#request body 
# {
#   "text": "I absolutely love this product! Best purchase ever.",
#   "detailed": true             // optional — if true, returns per-sentence breakdown
# }

#responce body 

# {
#   "overall_sentiment": "positive",
#   "confidence": 0.94,
#   "emotions": ["joy", "satisfaction"],
#   "breakdown": [
#     {
#       "sentence": "I absolutely love this product!",
#       "sentiment": "positive",
#       "confidence": 0.97
#     },
#     {
#       "sentence": "Best purchase ever.",
#       "sentiment": "positive",
#       "confidence": 0.91
#     }
#   ]
# }

class SentimentEnum(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class EmotionEnum(str, Enum):
    joy = "joy"
    satisfaction = "satisfaction"
    anger = "anger"
    sadness = "sadness"
    fear = "fear"
    surprise = "surprise"

class analyzerRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")
    detailed: bool = Field(False, description="If true, returns per-sentence breakdown")

class sentencebBreakdown(BaseModel):
    sentence: str
    sentiment: SentimentEnum
    confidence: float=Field(..., ge=0.00, le=0.99)

class analyzerResponse(BaseModel):
    overall_sentiment: SentimentEnum
    confidence: float
    emotions: list[EmotionEnum]
    breakdown: Optional[list[SentenceBreakdown]] = None  # only present when detailed=True