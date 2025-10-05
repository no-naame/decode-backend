"""
Schemas for data collection module
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DataCollectionRequest(BaseModel):
    """Request to collect data for a repository."""
    owner: str = Field(..., description="Repository owner (username or org)")
    repo: str = Field(..., description="Repository name")
    days: int = Field(default=30, ge=1, le=365, description="Number of days to look back")
    token: Optional[str] = Field(None, description="Optional GitHub token (overrides default)")


class DataCollectionStats(BaseModel):
    """Statistics from data collection."""
    repository_id: Optional[int]
    maintainers: int
    issues: int
    pull_requests: int
    pr_reviews: int
    pr_review_comments: int
    issue_comments: int
    issue_timeline_events: int
    discussions: int
    discussion_comments: int
    commits: int
    errors: List[str]
    collection_time: float  # seconds
    

class DataCollectionResponse(BaseModel):
    """Response from data collection."""
    success: bool
    message: str
    stats: Optional[DataCollectionStats]
    repository: Optional[Dict[str, Any]]


class RepositoryListResponse(BaseModel):
    """List of repositories in database."""
    total: int
    repositories: List[Dict[str, Any]]


class RepositoryStatsResponse(BaseModel):
    """Statistics for a specific repository."""
    repository: Dict[str, Any]
    stats: Dict[str, int]
    last_updated: Optional[datetime]

