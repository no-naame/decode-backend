"""
Data models matching the OpenAPI specification exactly.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# ============== Core Models ==============

class ActivityData(BaseModel):
    """Weekly activity breakdown"""
    date: str = Field(..., description="YYYY-MM-DD")
    reviews: int
    triage: int
    mentorship: int
    documentation: int
    discussions: int
    total: int


class TrendData(BaseModel):
    """Trend data point"""
    date: str = Field(..., description="YYYY-MM-DD")
    value: float
    label: Optional[str] = None


class CategoryData(BaseModel):
    """Activity category distribution"""
    category: str
    value: float
    percentage: float
    color: str = Field(..., description="Hex color code")


class MaintainerMetrics(BaseModel):
    """Complete maintainer metrics"""
    invisibleLaborScore: int = Field(..., ge=0, le=100)
    reviewImpactScore: int = Field(..., ge=0, le=100)
    communityEngagement: int = Field(..., ge=0, le=100)
    burnoutRisk: int = Field(..., ge=0, le=100)
    sentimentScore: int = Field(..., ge=0, le=100)
    totalRepositories: int
    responseTime: float = Field(..., description="Average response time in hours")
    totalContributions: int
    mentorshipHours: float
    weeklyActivity: List[ActivityData]
    sentimentTrend: List[TrendData]
    activityDistribution: List[CategoryData]


class BurnoutIndicators(BaseModel):
    """Burnout risk indicators"""
    workload: int = Field(..., ge=0, le=100)
    responseTime: int = Field(..., ge=0, le=100)
    sentimentDrop: int = Field(..., ge=0, le=100)
    activitySpikes: int = Field(..., ge=0, le=100)
    weekendWork: int = Field(..., ge=0, le=100)


class RecoveryMetrics(BaseModel):
    """Recovery tracking metrics"""
    daysOff: int
    delegatedTasks: int
    reducedScope: int


class BurnoutIndicator(BaseModel):
    """Burnout risk assessment"""
    riskScore: int = Field(..., ge=0, le=100)
    riskLevel: Literal["low", "medium", "high", "critical"]
    indicators: BurnoutIndicators
    recommendations: List[str]
    recoveryMetrics: RecoveryMetrics


class Achievement(BaseModel):
    """Achievement badge"""
    id: str
    title: str
    description: str
    icon: str
    level: Literal["bronze", "silver", "gold", "platinum"]
    earnedDate: str = Field(..., description="YYYY-MM-DD")
    category: str


class Skill(BaseModel):
    """Skill assessment"""
    skill: str
    score: float = Field(..., ge=0, le=100)
    maxScore: int = 100
    category: Literal["technical", "soft", "leadership"]


class Testimonial(BaseModel):
    """Community testimonial"""
    id: str
    author: str
    avatar: str
    content: str
    date: str = Field(..., description="YYYY-MM-DD")
    repository: str


class ImpactSummary(BaseModel):
    """Overall impact summary"""
    totalReviews: int
    issuesTriaged: int
    contributorsHelped: int
    documentationPages: int
    communityImpact: int = Field(..., ge=0, le=100)
    timeInvested: float = Field(..., description="Hours")


class TopRepository(BaseModel):
    """Top repository contribution"""
    repository: str
    role: str
    contributions: int
    impact: Literal["high", "medium", "low"]
    duration: str


class ContributionProfile(BaseModel):
    """Shareable contribution profile"""
    name: str
    username: str
    avatar: str
    bio: str
    joinedDate: str = Field(..., description="YYYY-MM-DD")
    achievements: List[Achievement]
    skills: List[Skill]
    testimonials: List[Testimonial]
    impactSummary: ImpactSummary
    topRepositories: List[TopRepository]


class TimelineEvent(BaseModel):
    """Activity timeline event"""
    id: str
    timestamp: str = Field(..., description="ISO 8601")
    type: Literal["review", "triage", "mentorship", "documentation", "discussion", "release"]
    title: str
    description: str
    repository: str
    impact: int = Field(..., ge=0, le=100)
    linkedPR: Optional[str] = None
    linkedIssue: Optional[str] = None


class WordFrequency(BaseModel):
    """Word frequency in feedback"""
    word: str
    count: int
    sentiment: Literal["positive", "negative", "neutral"]


class FeedbackDistribution(BaseModel):
    """Feedback tone distribution"""
    constructive: int
    appreciative: int
    critical: int
    neutral: int


class SentimentAnalysis(BaseModel):
    """Sentiment analysis results"""
    score: int = Field(..., ge=0, le=100)
    trend: Literal["improving", "stable", "declining"]
    wordFrequency: List[WordFrequency]
    feedbackDistribution: FeedbackDistribution
    topPositiveFeedback: List[str]
    concernAreas: List[str]


class CommunityMetric(BaseModel):
    """Community engagement metrics"""
    thankYouMessages: int
    helpedContributors: int
    mentorshipSessions: int
    conflictsResolved: int
    documentationImproved: int
    communityGrowth: int


class RepositoryHealth(BaseModel):
    """Repository health status"""
    id: str
    name: str
    healthScore: int = Field(..., ge=0, le=100)
    contributors: int
    activeContributors: int
    issuesResolved: int
    issuesOpen: int
    prsMerged: int
    prsOpen: int
    lastActivity: str
    responseTime: float
    sentiment: Literal["positive", "neutral", "negative"]
    stars: int
    forks: int


class Alert(BaseModel):
    """Dashboard alert"""
    id: str
    type: Literal["warning", "info", "critical"]
    title: str
    message: str
    timestamp: str = Field(..., description="ISO 8601")


# ============== API Response Models ==============

class DashboardOverviewResponse(BaseModel):
    """Main dashboard overview - SINGLE ENDPOINT RESPONSE"""
    metrics: MaintainerMetrics
    burnout: BurnoutIndicator
    sentiment: SentimentAnalysis
    communityMetrics: CommunityMetric
    profile: ContributionProfile
    alerts: List[Alert]
    recentActivity: List[TimelineEvent]
    repositoryHealth: List[RepositoryHealth]
