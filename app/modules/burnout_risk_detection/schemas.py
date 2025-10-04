from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class BurnoutIndicator(str, Enum):
    EXCESSIVE_HOURS = "excessive_hours"
    RAPID_RESPONSE_PRESSURE = "rapid_response_pressure"
    LACK_OF_BREAKS = "lack_of_breaks"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    DECREASED_ACTIVITY = "decreased_activity"
    INCREASED_CONFLICT = "increased_conflict"


class BurnoutRiskRequest(BaseModel):
    username: str
    repository: Optional[str] = None
    time_period_days: Optional[int] = 30


class BurnoutFactors(BaseModel):
    activity_score: float
    workload_score: float
    sentiment_score: float
    response_time_pressure: float
    work_life_balance: float


class BurnoutRiskResponse(BaseModel):
    username: str
    risk_level: RiskLevel
    risk_score: float  # 0 to 100
    factors: BurnoutFactors
    indicators: List[BurnoutIndicator]
    recommendations: List[str]
    timestamp: datetime


class BurnoutAlert(BaseModel):
    id: str
    username: str
    risk_level: RiskLevel
    indicator: BurnoutIndicator
    message: str
    created_at: datetime
    acknowledged: bool = False


class BurnoutHistoryEntry(BaseModel):
    date: str
    risk_score: float
    risk_level: RiskLevel
