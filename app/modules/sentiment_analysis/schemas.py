from pydantic import BaseModel
from typing import Optional, Dict, List
from enum import Enum


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class SentimentAnalysisRequest(BaseModel):
    repository: str
    username: Optional[str] = None
    time_period_days: Optional[int] = 30
    include_prs: bool = True
    include_issues: bool = True
    include_comments: bool = True


class SentimentScore(BaseModel):
    overall: SentimentType
    score: float  # -1 to 1
    confidence: float  # 0 to 1


class SentimentAnalysisResponse(BaseModel):
    repository: str
    sentiment: SentimentScore
    breakdown: Dict[str, SentimentScore]
    total_interactions: int
    time_period_days: int


class SentimentTrend(BaseModel):
    date: str
    sentiment_score: float
    interaction_count: int
