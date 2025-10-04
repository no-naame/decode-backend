from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime


class ContributionStats(BaseModel):
    total_commits: int
    total_prs: int
    total_issues: int
    code_reviews: int
    documentation_contributions: int
    community_support: int


class InvisibleContributions(BaseModel):
    invisible_labor_score: float
    mentoring_activities: int
    issue_triaging: int
    community_building: int


class ProfileHighlight(BaseModel):
    title: str
    description: str
    date: Optional[str] = None
    url: Optional[HttpUrl] = None


class ProfileRequest(BaseModel):
    username: str
    repositories: Optional[List[str]] = None
    include_invisible_labor: bool = True
    include_sentiment_data: bool = False
    custom_highlights: Optional[List[ProfileHighlight]] = None
    bio: Optional[str] = None


class ProfileResponse(BaseModel):
    username: str
    profile_id: str
    public_url: str
    contribution_stats: ContributionStats
    invisible_contributions: InvisibleContributions
    highlights: List[ProfileHighlight]
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProfileUpdateRequest(BaseModel):
    bio: Optional[str] = None
    custom_highlights: Optional[List[ProfileHighlight]] = None
    visibility: Optional[str] = "public"  # public, private, unlisted


class ProfileSettings(BaseModel):
    visibility: str
    show_invisible_labor: bool
    show_repositories: bool
    custom_theme: Optional[str] = None
