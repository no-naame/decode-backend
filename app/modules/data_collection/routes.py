"""
API routes for data collection
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.shared.database import get_db
from .schemas import (
    DataCollectionRequest, DataCollectionResponse, 
    DataCollectionStats, RepositoryListResponse,
    RepositoryStatsResponse
)
from .service import DataCollectionService

router = APIRouter(
    prefix="/data-collection",
    tags=["Data Collection"]
)

service = DataCollectionService()


@router.post("/collect", response_model=DataCollectionResponse)
async def collect_repository_data(
    request: DataCollectionRequest,
    db: Session = Depends(get_db)
):
    """
    Collect all available GitHub data for a repository.
    
    This endpoint fetches:
    - Repository information
    - Issues and their comments
    - Pull requests, reviews, and review comments
    - Issue timeline events (triage activity)
    - Discussions and discussion comments (GraphQL)
    - Commits
    - Maintainer information
    
    Data is collected for the last N days (default: 30 days).
    """
    try:
        stats = await service.collect_repository_data(
            db=db,
            owner=request.owner,
            repo=request.repo,
            days=request.days,
            token=request.token
        )
        
        # Get repository info
        repository = service.get_repository_stats(db, request.owner, request.repo)
        
        return DataCollectionResponse(
            success=True,
            message=f"Successfully collected data for {request.owner}/{request.repo}",
            stats=DataCollectionStats(
                repository_id=stats.get('repository'),
                maintainers=stats.get('maintainers', 0),
                issues=stats.get('issues', 0),
                pull_requests=stats.get('pull_requests', 0),
                pr_reviews=stats.get('pr_reviews', 0),
                pr_review_comments=stats.get('pr_review_comments', 0),
                issue_comments=stats.get('issue_comments', 0),
                issue_timeline_events=stats.get('issue_timeline_events', 0),
                discussions=stats.get('discussions', 0),
                discussion_comments=stats.get('discussion_comments', 0),
                commits=stats.get('commits', 0),
                errors=stats.get('errors', []),
                collection_time=stats.get('collection_time', 0),
            ),
            repository=repository.get('repository') if repository else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error collecting data: {str(e)}"
        )


@router.get("/repositories", response_model=RepositoryListResponse)
def list_repositories(db: Session = Depends(get_db)):
    """
    List all repositories in the database.
    
    Returns basic information and last fetch time for each repository.
    """
    try:
        result = service.list_repositories(db)
        return RepositoryListResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing repositories: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/stats", response_model=RepositoryStatsResponse)
def get_repository_stats(
    owner: str,
    repo: str,
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific repository.
    
    Returns counts of all data types stored for this repository.
    """
    try:
        stats = service.get_repository_stats(db, owner, repo)
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository {owner}/{repo} not found in database"
            )
        
        return RepositoryStatsResponse(
            repository=stats['repository'],
            stats=stats['counts'],
            last_updated=stats['repository'].get('last_fetched')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting repository stats: {str(e)}"
        )


@router.get("/maintainers")
def list_maintainers(
    repository_id: int = None,
    db: Session = Depends(get_db)
):
    """
    List all maintainers in the database.
    
    Optionally filter by repository ID.
    """
    try:
        result = service.get_maintainers(db, repository_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing maintainers: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/data")
def get_repository_data(
    owner: str,
    repo: str,
    db: Session = Depends(get_db)
):
    """
    Get ALL collected data for a repository.
    
    Returns complete data including issues, PRs, reviews, comments, etc.
    """
    from app.shared.models import (
        Repository, Maintainer, Issue, PullRequest, PRReview,
        PRReviewComment, IssueComment, IssueTimelineEvent,
        Discussion, DiscussionComment, Commit
    )
    
    try:
        full_name = f"{owner}/{repo}"
        repository = db.query(Repository).filter(Repository.full_name == full_name).first()
        
        if not repository:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository {owner}/{repo} not found in database"
            )
        
        # Get all data
        issues = db.query(Issue).filter(Issue.repository_id == repository.id).all()
        prs = db.query(PullRequest).filter(PullRequest.repository_id == repository.id).all()
        pr_reviews = db.query(PRReview).join(PullRequest).filter(PullRequest.repository_id == repository.id).all()
        pr_review_comments = db.query(PRReviewComment).join(PullRequest).filter(PullRequest.repository_id == repository.id).all()
        issue_comments = db.query(IssueComment).join(Issue).filter(Issue.repository_id == repository.id).all()
        timeline_events = db.query(IssueTimelineEvent).join(Issue).filter(Issue.repository_id == repository.id).all()
        discussions = db.query(Discussion).filter(Discussion.repository_id == repository.id).all()
        discussion_comments = db.query(DiscussionComment).join(Discussion).filter(Discussion.repository_id == repository.id).all()
        commits = db.query(Commit).filter(Commit.repository_id == repository.id).all()
        
        # Get unique maintainers
        maintainer_ids = set()
        for issue in issues:
            if issue.created_by: maintainer_ids.add(issue.created_by)
        for pr in prs:
            if pr.created_by: maintainer_ids.add(pr.created_by)
        for review in pr_reviews:
            if review.reviewer_id: maintainer_ids.add(review.reviewer_id)
        
        maintainers = db.query(Maintainer).filter(Maintainer.id.in_(maintainer_ids)).all() if maintainer_ids else []
        
        return {
            "success": True,
            "repository": {
                "id": repository.id,
                "name": repository.name,
                "full_name": repository.full_name,
                "description": repository.description,
                "stars": repository.stars,
                "forks": repository.forks,
                "language": repository.language,
                "last_fetched": repository.fetched_at.isoformat() if repository.fetched_at else None
            },
            "maintainers": [
                {
                    "id": m.id,
                    "username": m.username,
                    "name": m.name,
                    "email": m.email,
                    "company": m.company,
                    "location": m.location,
                    "avatar_url": m.avatar_url
                }
                for m in maintainers
            ],
            "issues": [
                {
                    "number": i.number,
                    "title": i.title,
                    "state": i.state,
                    "labels": i.labels,
                    "comments_count": i.comments_count,
                    "created_at": i.created_at.isoformat() if i.created_at else None
                }
                for i in issues
            ],
            "pull_requests": [
                {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "merged": pr.merged,
                    "commits_count": pr.commits_count,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "created_at": pr.created_at.isoformat() if pr.created_at else None
                }
                for pr in prs
            ],
            "pr_reviews": [
                {
                    "state": r.state,
                    "submitted_at": r.submitted_at.isoformat() if r.submitted_at else None
                }
                for r in pr_reviews
            ],
            "pr_review_comments": len(pr_review_comments),
            "issue_comments": len(issue_comments),
            "timeline_events": len(timeline_events),
            "discussions": len(discussions),
            "discussion_comments": len(discussion_comments),
            "commits": len(commits),
            "counts": {
                "maintainers": len(maintainers),
                "issues": len(issues),
                "pull_requests": len(prs),
                "pr_reviews": len(pr_reviews),
                "pr_review_comments": len(pr_review_comments),
                "issue_comments": len(issue_comments),
                "timeline_events": len(timeline_events),
                "discussions": len(discussions),
                "discussion_comments": len(discussion_comments),
                "commits": len(commits)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting repository data: {str(e)}"
        )


@router.delete("/repositories/{owner}/{repo}")
def delete_repository_data(
    owner: str,
    repo: str,
    db: Session = Depends(get_db)
):
    """
    Delete all data for a repository from the database.
    
    Warning: This will delete all associated data (issues, PRs, reviews, etc.)
    """
    from app.shared.models import Repository
    
    try:
        full_name = f"{owner}/{repo}"
        repository = db.query(Repository).filter(Repository.full_name == full_name).first()
        
        if not repository:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository {owner}/{repo} not found"
            )
        
        # Delete repository (cascade will delete all related data)
        db.delete(repository)
        db.commit()
        
        return {
            "success": True,
            "message": f"Successfully deleted all data for {owner}/{repo}"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting repository: {str(e)}"
        )

