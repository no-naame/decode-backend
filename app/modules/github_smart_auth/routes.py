"""
GitHub Smart Authentication Routes

FastAPI routes for GitHub smart authentication operations.
"""

from fastapi import APIRouter, HTTPException, status, Query, Path, Body
from typing import List, Dict, Any, Optional
import logging

from app.modules.github_smart_auth.service import github_smart_auth_service
from app.modules.github_smart_auth.schemas import (
    GitHubAppInfo,
    GitHubInstallationsResponse,
    GitHubRepositoriesResponse,
    GitHubRepositoryResponse,
    GitHubContentsResponse,
    GitHubFileResponse,
    GitHubBranchesResponse,
    GitHubCommitsResponse,
    GitHubIssuesResponse,
    CreateIssueRequest,
    GitHubIssueResponse,
    GitHubWebhookResponse
)
from app.modules.github_smart_auth.installation_routes import router as installation_router

logger = logging.getLogger(__name__)

router = APIRouter()

# Include installation routes
router.include_router(installation_router, tags=["installation"])


@router.get("/app/info", response_model=GitHubAppInfo)
async def get_app_info():
    """Get GitHub App information (app-level operation)"""
    try:
        result = github_smart_auth_service.get_app_info()
        return GitHubAppInfo(**result)
    except Exception as e:
        logger.error(f"Failed to get app info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get app info: {str(e)}"
        )


@router.get("/app/installations", response_model=GitHubInstallationsResponse)
async def get_all_installations():
    """Get all installations of the GitHub App (app-level operation)"""
    try:
        result = github_smart_auth_service.get_all_installations()
        return GitHubInstallationsResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get installations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get installations: {str(e)}"
        )


@router.get("/repositories", response_model=GitHubRepositoriesResponse)
async def get_repositories(
    organization: Optional[str] = Query(None, description="Filter by organization"),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Get repositories - automatically determines the right installation"""
    try:
        result = github_smart_auth_service.get_repositories(organization, installation_id)
        return GitHubRepositoriesResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get repositories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get repositories: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}", response_model=GitHubRepositoryResponse)
async def get_repository(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Get repository details - automatically finds the right installation"""
    try:
        result = github_smart_auth_service.get_repository(owner, repo, installation_id)
        return GitHubRepositoryResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get repository {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get repository: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/contents", response_model=GitHubContentsResponse)
async def get_repository_contents(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    path: str = Query("", description="Path within the repository"),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Get repository contents - automatically finds the right installation"""
    try:
        result = github_smart_auth_service.get_repository_contents(owner, repo, path, installation_id)
        return GitHubContentsResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get repository contents {owner}/{repo}/{path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get repository contents: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/file", response_model=GitHubFileResponse)
async def get_file_content(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    file_path: str = Query(..., description="Path to the file"),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Get file content - automatically finds the right installation"""
    try:
        result = github_smart_auth_service.get_file_content(owner, repo, file_path, installation_id)
        return GitHubFileResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get file content {owner}/{repo}/{file_path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file content: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/branches", response_model=GitHubBranchesResponse)
async def get_branches(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Get repository branches - automatically finds the right installation"""
    try:
        result = github_smart_auth_service.get_branches(owner, repo, installation_id)
        return GitHubBranchesResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get branches {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get branches: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/commits", response_model=GitHubCommitsResponse)
async def get_commits(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    branch: str = Query("main", description="Branch name"),
    limit: int = Query(10, description="Number of commits to return", ge=1, le=100),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Get repository commits - automatically finds the right installation"""
    try:
        result = github_smart_auth_service.get_commits(owner, repo, branch, limit, installation_id)
        return GitHubCommitsResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get commits {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get commits: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/issues", response_model=GitHubIssuesResponse)
async def get_issues(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    state: str = Query("open", description="Issue state (open, closed, all)"),
    limit: int = Query(10, description="Number of issues to return", ge=1, le=100),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Get repository issues - automatically finds the right installation"""
    try:
        result = github_smart_auth_service.get_issues(owner, repo, state, limit, installation_id)
        return GitHubIssuesResponse(**result)
    except Exception as e:
        logger.error(f"Failed to get issues {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get issues: {str(e)}"
        )


@router.post("/repositories/{owner}/{repo}/issues", response_model=GitHubIssueResponse)
async def create_issue(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    issue_data: CreateIssueRequest = Body(...),
    installation_id: Optional[str] = Query(None, description="Specific installation ID")
):
    """Create issue in repository - automatically finds the right installation"""
    try:
        result = github_smart_auth_service.create_issue(
            owner, 
            repo, 
            issue_data.title, 
            issue_data.body, 
            issue_data.labels, 
            installation_id
        )
        return GitHubIssueResponse(**result)
    except Exception as e:
        logger.error(f"Failed to create issue {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create issue: {str(e)}"
        )


@router.post("/webhooks/github", response_model=GitHubWebhookResponse)
async def github_webhook(
    payload: Dict[str, Any] = Body(...),
    x_github_event: str = Query(None, description="GitHub event type")
):
    """Handle GitHub webhooks - automatically extracts installation ID from webhook payload"""
    try:
        result = github_smart_auth_service.process_webhook(payload)
        return GitHubWebhookResponse(**result)
    except Exception as e:
        logger.error(f"Failed to process webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )
