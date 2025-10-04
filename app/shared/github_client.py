from typing import Optional, Dict, List
import httpx
from app.core.config import settings


class GitHubClient:
    """
    Shared GitHub API client for all modules.

    Usage:
    client = GitHubClient()
    user_data = await client.get_user("username")
    """

    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make API request to GitHub."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{endpoint}"
            response = await client.request(
                method,
                url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def get_user(self, username: str) -> Dict:
        """Get user information."""
        return await self._request("GET", f"users/{username}")

    async def get_user_repos(self, username: str) -> List[Dict]:
        """Get user repositories."""
        return await self._request("GET", f"users/{username}/repos")

    async def get_repo(self, owner: str, repo: str) -> Dict:
        """Get repository information."""
        return await self._request("GET", f"repos/{owner}/{repo}")

    async def get_commits(self, owner: str, repo: str, author: Optional[str] = None) -> List[Dict]:
        """Get repository commits."""
        params = {}
        if author:
            params["author"] = author
        return await self._request("GET", f"repos/{owner}/{repo}/commits", params=params)

    async def get_pull_requests(self, owner: str, repo: str, state: str = "all") -> List[Dict]:
        """Get repository pull requests."""
        return await self._request("GET", f"repos/{owner}/{repo}/pulls", params={"state": state})

    async def get_issues(self, owner: str, repo: str, state: str = "all") -> List[Dict]:
        """Get repository issues."""
        return await self._request("GET", f"repos/{owner}/{repo}/issues", params={"state": state})

    async def get_issue_comments(self, owner: str, repo: str, issue_number: int) -> List[Dict]:
        """Get comments for a specific issue."""
        return await self._request("GET", f"repos/{owner}/{repo}/issues/{issue_number}/comments")

    async def get_pr_reviews(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """Get reviews for a specific pull request."""
        return await self._request("GET", f"repos/{owner}/{repo}/pulls/{pr_number}/reviews")
