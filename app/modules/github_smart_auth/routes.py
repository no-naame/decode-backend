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
from app.shared.github_client import GitHubClient
from app.shared.smart_github_auth import smart_github_auth_service
import httpx

logger = logging.getLogger(__name__)

router = APIRouter()

# Include installation routes
router.include_router(installation_router, tags=["installation"])

# Initialize GitHub client for GraphQL operations
github_client = GitHubClient()

class GitHubAppGraphQLClient:
    """GraphQL client that uses GitHub App authentication"""
    
    def __init__(self):
        self.graphql_url = "https://api.github.com/graphql"
        self.auth_service = smart_github_auth_service
    
    async def _make_graphql_request(self, query: str, variables: Optional[Dict[str, Any]] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GraphQL request using GitHub App authentication"""
        try:
            # For GraphQL queries, we need installation-level authentication
            # Try to get installation-level headers first
            if context:
                headers = self.auth_service.smart_authenticate(context)
            else:
                # For GraphQL queries without context, try to use any available installation
                # or fall back to app-level (which may not work for all queries)
                installations = self.auth_service.get_all_installations()
                if installations and len(installations) > 0:
                    # Use the first available installation
                    installation_id = str(installations[0]['id'])
                    headers = self.auth_service.get_installation_headers(installation_id)
                else:
                    # Fallback to app-level (may not work for user/org queries)
                    headers = self.auth_service.get_app_level_headers()
            
            # Update headers for GraphQL
            headers.update({
                "Content-Type": "application/json",
                "Accept": "application/vnd.github.v4+json"
            })
            
            payload = {"query": query}
            if variables:
                payload["variables"] = variables
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.graphql_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"GraphQL request failed: {e}")
            raise
    
    async def get_user_contributions(self, username: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """Get user contribution data using GraphQL with GitHub App auth"""
        query = """
        query($username: String!, $from: DateTime!, $to: DateTime!) {
            user(login: $username) {
                name
                login
                contributionsCollection(from: $from, to: $to) {
                    totalCommitContributions
                    totalIssueContributions
                    totalPullRequestContributions
                    totalPullRequestReviewContributions
                    contributionCalendar {
                        totalContributions
                        weeks {
                            contributionDays {
                                date
                                contributionCount
                                weekday
                            }
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "username": username,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z"
        }
        
        # For user queries, we need installation-level auth
        # Try to find an installation that might have access to this user's data
        context = {'username': username}
        return await self._make_graphql_request(query, variables, context)
    
    async def get_user_repositories_detailed(self, username: str, first: int = 20) -> Dict[str, Any]:
        """Get detailed user repositories using GraphQL with GitHub App auth"""
        query = """
        query($username: String!, $first: Int!) {
            user(login: $username) {
                repositories(first: $first, orderBy: {field: UPDATED_AT, direction: DESC}) {
                    totalCount
                    nodes {
                        name
                        description
                        url
                        stargazerCount
                        forkCount
                        watchers {
                            totalCount
                        }
                        languages(first: 10) {
                            nodes {
                                name
                                color
                            }
                        }
                        repositoryTopics(first: 10) {
                            nodes {
                                topic {
                                    name
                                }
                            }
                        }
                        defaultBranchRef {
                            name
                            target {
                                ... on Commit {
                                    history(first: 1) {
                                        nodes {
                                            committedDate
                                        }
                                    }
                                }
                            }
                        }
                        createdAt
                        updatedAt
                    }
                }
            }
        }
        """
        
        variables = {
            "username": username,
            "first": min(first, 100)
        }
        
        # For user queries, we need installation-level auth
        context = {'username': username}
        return await self._make_graphql_request(query, variables, context)
    
    async def get_repository_analytics(self, owner: str, repo: str, since: str) -> Dict[str, Any]:
        """Get repository analytics using GraphQL with GitHub App auth"""
        query = """
        query($owner: String!, $repo: String!, $since: GitTimestamp!) {
            repository(owner: $owner, name: $repo) {
                name
                description
                stargazerCount
                forkCount
                watchers {
                    totalCount
                }
                defaultBranchRef {
                    name
                    target {
                        ... on Commit {
                            history(since: $since) {
                                totalCount
                                nodes {
                                    message
                                    author {
                                        name
                                        email
                                        date
                                    }
                                    additions
                                    deletions
                                }
                            }
                        }
                    }
                }
                pullRequests(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                    totalCount
                    nodes {
                        title
                        state
                        createdAt
                        author {
                            login
                        }
                        additions
                        deletions
                    }
                }
                issues(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                    totalCount
                    nodes {
                        title
                        state
                        createdAt
                        author {
                            login
                        }
                    }
                }
                collaborators(first: 50) {
                    totalCount
                    nodes {
                        login
                        name
                    }
                }
            }
        }
        """
        
        variables = {
            "owner": owner,
            "repo": repo,
            "since": since
        }
        
        # Use repository context for smart authentication
        context = {'owner': owner, 'repo': repo}
        return await self._make_graphql_request(query, variables, context)
    
    async def get_organization_members(self, org: str, first: int = 50) -> Dict[str, Any]:
        """Get organization members using GraphQL with GitHub App auth"""
        query = """
        query($org: String!, $first: Int!) {
            organization(login: $org) {
                name
                membersWithRole(first: $first) {
                    totalCount
                    nodes {
                        login
                        name
                        avatarUrl
                        contributionsCollection {
                            totalCommitContributions
                            totalIssueContributions
                            totalPullRequestContributions
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "org": org,
            "first": min(first, 100)
        }
        
        # Use organization context for smart authentication
        context = {'org': org}
        return await self._make_graphql_request(query, variables, context)
    
    async def search_repositories(self, query: str, first: int = 20) -> Dict[str, Any]:
        """Search repositories using GraphQL with GitHub App auth"""
        graphql_query = """
        query($query: String!, $first: Int!) {
            search(query: $query, type: REPOSITORY, first: $first) {
                repositoryCount
                nodes {
                    ... on Repository {
                        name
                        nameWithOwner
                        description
                        url
                        stargazerCount
                        forkCount
                        languages(first: 5) {
                            nodes {
                                name
                                color
                            }
                        }
                        owner {
                            login
                            avatarUrl
                        }
                        createdAt
                        updatedAt
                    }
                }
            }
        }
        """
        
        variables = {
            "query": query,
            "first": min(first, 100)
        }
        
        # For search queries, we need installation-level auth
        context = {'search_query': query}
        return await self._make_graphql_request(graphql_query, variables, context)
    
    async def get_discussion_categories(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get discussion categories using GraphQL with GitHub App auth"""
        query = """
        query($owner: String!, $repo: String!) {
            repository(owner: $owner, name: $repo) {
                name
                discussionCategories(first: 20) {
                    totalCount
                    nodes {
                        id
                        name
                        description
                        emoji
                        isAnswerable
                    }
                }
            }
        }
        """
        
        variables = {
            "owner": owner,
            "repo": repo
        }
        
        context = {'owner': owner, 'repo': repo}
        return await self._make_graphql_request(query, variables, context)
    
    async def get_repository_discussions(self, owner: str, repo: str, first: int = 20, category: Optional[str] = None) -> Dict[str, Any]:
        """Get repository discussions using GraphQL with GitHub App auth"""
        query = """
        query($owner: String!, $repo: String!, $first: Int!, $category: ID) {
            repository(owner: $owner, name: $repo) {
                name
                discussions(first: $first, categoryId: $category, orderBy: {field: CREATED_AT, direction: DESC}) {
                    totalCount
                    nodes {
                        id
                        title
                        body
                        bodyText
                        bodyHTML
                        createdAt
                        updatedAt
                        publishedAt
                        number
                        author {
                            ... on User {
                                login
                                name
                                avatarUrl
                            }
                        }
                        category {
                            id
                            name
                            description
                        }
                        answer {
                            id
                            body
                            author {
                                ... on User {
                                    login
                                    name
                                }
                            }
                            createdAt
                        }
                        comments(first: 10) {
                            totalCount
                            nodes {
                                id
                                body
                                createdAt
                                author {
                                    ... on User {
                                        login
                                        name
                                        avatarUrl
                                    }
                                }
                                reactions(first: 10) {
                                    totalCount
                                    nodes {
                                        content
                                        user {
                                            login
                                        }
                                    }
                                }
                            }
                        }
                        reactions(first: 10) {
                            totalCount
                            nodes {
                                content
                                user {
                                    login
                                }
                            }
                        }
                        labels(first: 10) {
                            totalCount
                            nodes {
                                name
                                color
                            }
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "owner": owner,
            "repo": repo,
            "first": min(first, 100)
        }
        
        if category:
            variables["category"] = category
        
        context = {'owner': owner, 'repo': repo}
        return await self._make_graphql_request(query, variables, context)
    
    async def get_discussion_by_number(self, owner: str, repo: str, number: int) -> Dict[str, Any]:
        """Get specific discussion using GraphQL with GitHub App auth"""
        query = """
        query($owner: String!, $repo: String!, $number: Int!) {
            repository(owner: $owner, name: $repo) {
                discussion(number: $number) {
                    id
                    title
                    body
                    bodyText
                    bodyHTML
                    createdAt
                    updatedAt
                    publishedAt
                    number
                    author {
                        ... on User {
                            login
                            name
                            avatarUrl
                        }
                    }
                    category {
                        id
                        name
                        description
                    }
                    answer {
                        id
                        body
                        author {
                            ... on User {
                                login
                                name
                            }
                        }
                        createdAt
                    }
                    comments(first: 50) {
                        totalCount
                        nodes {
                            id
                            body
                            createdAt
                            author {
                                ... on User {
                                    login
                                    name
                                    avatarUrl
                                }
                            }
                            reactions(first: 20) {
                                totalCount
                                nodes {
                                    content
                                    user {
                                        login
                                    }
                                }
                            }
                        }
                    }
                    reactions(first: 20) {
                        totalCount
                        nodes {
                            content
                            user {
                                login
                            }
                        }
                    }
                    labels(first: 20) {
                        totalCount
                        nodes {
                            name
                            color
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "owner": owner,
            "repo": repo,
            "number": number
        }
        
        context = {'owner': owner, 'repo': repo}
        return await self._make_graphql_request(query, variables, context)
    
    async def search_discussions(self, query: str, first: int = 20) -> Dict[str, Any]:
        """Search discussions using GraphQL with GitHub App auth"""
        graphql_query = """
        query($query: String!, $first: Int!) {
            search(query: $query, type: DISCUSSION, first: $first) {
                discussionCount
                nodes {
                    ... on Discussion {
                        id
                        title
                        body
                        createdAt
                        updatedAt
                        number
                        author {
                            ... on User {
                                login
                                name
                                avatarUrl
                            }
                        }
                        repository {
                            name
                            nameWithOwner
                            owner {
                                login
                            }
                        }
                        category {
                            name
                            description
                        }
                        comments {
                            totalCount
                        }
                        reactions {
                            totalCount
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "query": query,
            "first": min(first, 100)
        }
        
        return await self._make_graphql_request(graphql_query, variables)

# Initialize GitHub App GraphQL client
github_app_graphql_client = GitHubAppGraphQLClient()


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


# ==================== GraphQL v4 Analytics Endpoints ====================

@router.get("/graphql/contributions")
async def get_user_contributions(
    username: str = Query(..., description="GitHub username"),
    from_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(..., description="End date (YYYY-MM-DD)")
):
    """Get user contribution data using GraphQL with GitHub App auth"""
    try:
        result = await github_app_graphql_client.get_user_contributions(username, from_date, to_date)
        return result
    except Exception as e:
        logger.error(f"Failed to get user contributions for {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user contributions: {str(e)}"
        )


@router.get("/graphql/repositories")
async def get_user_repositories_detailed(
    username: str = Query(..., description="GitHub username"),
    first: int = Query(10, description="Number of repositories to fetch")
):
    """Get detailed user repositories using GraphQL"""
    try:
        result = await github_app_graphql_client.get_user_repositories_detailed(username, first)
        return result
    except Exception as e:
        logger.error(f"Failed to get detailed repositories for {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get detailed repositories: {str(e)}"
        )


@router.get("/graphql/analytics")
async def get_repository_analytics(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    since: str = Query(..., description="Since date (ISO format)")
):
    """Get repository analytics using GraphQL"""
    try:
        result = await github_app_graphql_client.get_repository_analytics(owner, repo, since)
        return result
    except Exception as e:
        logger.error(f"Failed to get repository analytics for {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get repository analytics: {str(e)}"
        )


@router.get("/graphql/org-members")
async def get_organization_members(
    org: str = Query(..., description="Organization name"),
    first: int = Query(20, description="Number of members to fetch")
):
    """Get organization members using GraphQL"""
    try:
        result = await github_app_graphql_client.get_organization_members(org, first)
        return result
    except Exception as e:
        logger.error(f"Failed to get organization members for {org}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get organization members: {str(e)}"
        )


@router.get("/graphql/search")
async def search_repositories(
    query: str = Query(..., description="Search query"),
    first: int = Query(10, description="Number of results to return")
):
    """Search repositories using GraphQL"""
    try:
        result = await github_app_graphql_client.search_repositories(query, first)
        return result
    except Exception as e:
        logger.error(f"Failed to search repositories with query '{query}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search repositories: {str(e)}"
        )


# ==================== GitHub Discussions Endpoints ====================

@router.get("/discussions/categories")
async def get_discussion_categories(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name")
):
    """Get discussion categories using GraphQL"""
    try:
        result = await github_app_graphql_client.get_discussion_categories(owner, repo)
        return result
    except Exception as e:
        logger.error(f"Failed to get discussion categories for {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get discussion categories: {str(e)}"
        )


@router.get("/discussions")
async def get_repository_discussions(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    first: int = Query(10, description="Number of discussions to fetch"),
    category: Optional[str] = Query(None, description="Discussion category filter")
):
    """Get repository discussions using GraphQL"""
    try:
        result = await github_app_graphql_client.get_repository_discussions(owner, repo, first, category)
        return result
    except Exception as e:
        logger.error(f"Failed to get discussions for {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get discussions: {str(e)}"
        )


@router.get("/discussions/{owner}/{repo}/{number}")
async def get_specific_discussion(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    number: int = Path(..., description="Discussion number")
):
    """Get specific discussion using GraphQL"""
    try:
        result = await github_app_graphql_client.get_discussion_by_number(owner, repo, number)
        return result
    except Exception as e:
        logger.error(f"Failed to get discussion {owner}/{repo}#{number}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get discussion: {str(e)}"
        )


@router.get("/discussions/search")
async def search_discussions(
    query: str = Query(..., description="Search query"),
    first: int = Query(10, description="Number of results to return")
):
    """Search discussions using GraphQL"""
    try:
        result = await github_app_graphql_client.search_discussions(query, first)
        return result
    except Exception as e:
        logger.error(f"Failed to search discussions with query '{query}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search discussions: {str(e)}"
        )
