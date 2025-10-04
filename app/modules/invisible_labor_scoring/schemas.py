from pydantic import BaseModel
from typing import Optional, Dict, Any


class InvisibleLaborScoreRequest(BaseModel):
    username: str
    repository: Optional[str] = None
    time_period_days: Optional[int] = 30


class InvisibleLaborScoreResponse(BaseModel):
    username: str
    total_score: float
    breakdown: Dict[str, Any]
    time_period_days: int


class InvisibleLaborMetrics(BaseModel):
    code_reviews: int
    issue_triaging: int
    documentation_updates: int
    community_support: int
    mentoring_activities: int
