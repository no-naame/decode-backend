"""
Service layer for data collection
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.shared.github_data_collector import GitHubDataCollector
from app.shared.models import (
    Repository, Maintainer, Issue, PullRequest, PRReview, 
    PRReviewComment, IssueComment, IssueTimelineEvent, 
    Discussion, DiscussionComment, Commit
)
import time


class DataCollectionService:
    """Service for collecting and managing GitHub data."""

    async def collect_repository_data(
        self,
        db: Session,
        owner: str,
        repo: str,
        days: int = 30,
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Collect all available GitHub data for a repository.
        
        Args:
            db: Database session
            owner: Repository owner
            repo: Repository name
            days: Number of days to look back
            token: Optional GitHub token
            
        Returns:
            Collection statistics
        """
        start_time = time.time()
        
        collector = GitHubDataCollector(token=token)
        stats = await collector.collect_repository_data(db, owner, repo, days)
        
        collection_time = time.time() - start_time
        stats['collection_time'] = collection_time
        
        return stats

    def get_repository_stats(self, db: Session, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get statistics for a repository from database.
        
        Args:
            db: Database session
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository statistics
        """
        full_name = f"{owner}/{repo}"
        repository = db.query(Repository).filter(Repository.full_name == full_name).first()
        
        if not repository:
            return None
        
        stats = {
            "repository": {
                "id": repository.id,
                "name": repository.name,
                "full_name": repository.full_name,
                "description": repository.description,
                "stars": repository.stars,
                "forks": repository.forks,
                "language": repository.language,
                "created_at": repository.created_at.isoformat() if repository.created_at else None,
                "last_fetched": repository.fetched_at.isoformat() if repository.fetched_at else None,
            },
            "counts": {
                "issues": db.query(Issue).filter(Issue.repository_id == repository.id).count(),
                "pull_requests": db.query(PullRequest).filter(PullRequest.repository_id == repository.id).count(),
                "pr_reviews": db.query(PRReview).join(PullRequest).filter(PullRequest.repository_id == repository.id).count(),
                "pr_review_comments": db.query(PRReviewComment).join(PullRequest).filter(PullRequest.repository_id == repository.id).count(),
                "issue_comments": db.query(IssueComment).join(Issue).filter(Issue.repository_id == repository.id).count(),
                "timeline_events": db.query(IssueTimelineEvent).join(Issue).filter(Issue.repository_id == repository.id).count(),
                "discussions": db.query(Discussion).filter(Discussion.repository_id == repository.id).count(),
                "discussion_comments": db.query(DiscussionComment).join(Discussion).filter(Discussion.repository_id == repository.id).count(),
                "commits": db.query(Commit).filter(Commit.repository_id == repository.id).count(),
            }
        }
        
        return stats

    def list_repositories(self, db: Session) -> Dict[str, Any]:
        """
        List all repositories in database.
        
        Args:
            db: Database session
            
        Returns:
            List of repositories with counts
        """
        repositories = db.query(Repository).all()
        
        result = []
        for repo in repositories:
            result.append({
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "stars": repo.stars,
                "forks": repo.forks,
                "language": repo.language,
                "last_fetched": repo.fetched_at.isoformat() if repo.fetched_at else None,
            })
        
        return {
            "total": len(result),
            "repositories": result
        }

    def get_maintainers(self, db: Session, repository_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get maintainers, optionally filtered by repository.
        
        Args:
            db: Database session
            repository_id: Optional repository ID to filter by
            
        Returns:
            List of maintainers
        """
        query = db.query(Maintainer)
        
        if repository_id:
            # Get maintainers who have contributed to this repository
            maintainer_ids = set()
            
            # From issues
            issue_creators = db.query(Issue.created_by).filter(Issue.repository_id == repository_id).distinct()
            maintainer_ids.update([m[0] for m in issue_creators if m[0]])
            
            # From PRs
            pr_creators = db.query(PullRequest.created_by).filter(PullRequest.repository_id == repository_id).distinct()
            maintainer_ids.update([m[0] for m in pr_creators if m[0]])
            
            # From reviews
            reviewers = db.query(PRReview.reviewer_id).join(PullRequest).filter(PullRequest.repository_id == repository_id).distinct()
            maintainer_ids.update([m[0] for m in reviewers if m[0]])
            
            query = query.filter(Maintainer.id.in_(maintainer_ids))
        
        maintainers = query.all()
        
        result = []
        for maintainer in maintainers:
            result.append({
                "id": maintainer.id,
                "username": maintainer.username,
                "name": maintainer.name,
                "email": maintainer.email,
                "avatar_url": maintainer.avatar_url,
                "company": maintainer.company,
                "location": maintainer.location,
            })
        
        return {
            "total": len(result),
            "maintainers": result
        }

