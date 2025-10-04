from typing import Optional, Dict, List, Any
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
        self.graphql_url = "https://api.github.com/graphql"
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

    # ==================== GraphQL v4 API Methods ====================
    
    async def graphql_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query against GitHub's GraphQL API v4.
        
        Args:
            query: GraphQL query string
            variables: Optional variables for the query
            
        Returns:
            Dict containing the GraphQL response data
            
        Example:
            query = '''
                query($username: String!) {
                    user(login: $username) {
                        name
                        login
                        contributionsCollection {
                            totalCommitContributions
                        }
                    }
                }
            '''
            result = await client.graphql_query(query, {"username": "octocat"})
        """
        headers = {
            **self.headers,
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v4+json"  # GraphQL v4
        }
        
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
    
    async def get_user_contributions(self, username: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get user contribution data using GraphQL.
        
        Args:
            username: GitHub username
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            User contribution data including commits, PRs, issues, etc.
        """
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
        
        return await self.graphql_query(query, variables)
    
    async def get_repository_analytics(self, owner: str, repo: str, since: str) -> Dict[str, Any]:
        """
        Get comprehensive repository analytics using GraphQL.
        
        Args:
            owner: Repository owner
            repo: Repository name
            since: ISO date string (e.g., "2024-01-01T00:00:00Z")
            
        Returns:
            Repository analytics including commits, PRs, issues, contributors
        """
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
        
        return await self.graphql_query(query, variables)
    
    async def get_user_repositories_detailed(self, username: str, first: int = 20) -> Dict[str, Any]:
        """
        Get detailed user repositories with advanced metrics using GraphQL.
        
        Args:
            username: GitHub username
            first: Number of repositories to fetch (max 100)
            
        Returns:
            Detailed repository information including languages, topics, etc.
        """
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
            "first": min(first, 100)  # GitHub limit
        }
        
        return await self.graphql_query(query, variables)
    
    async def get_organization_members(self, org: str, first: int = 50) -> Dict[str, Any]:
        """
        Get organization members with their contribution data using GraphQL.
        
        Args:
            org: Organization name
            first: Number of members to fetch (max 100)
            
        Returns:
            Organization members with their contribution statistics
        """
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
        
        return await self.graphql_query(query, variables)
    
    async def search_repositories(self, query: str, first: int = 20) -> Dict[str, Any]:
        """
        Search repositories using GraphQL.
        
        Args:
            query: Search query (e.g., "language:python stars:>1000")
            first: Number of results to return (max 100)
            
        Returns:
            Search results with repository details
        """
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
        
        return await self.graphql_query(graphql_query, variables)
    
    # ==================== GitHub Discussions (GraphQL Only) ====================
    
    async def get_repository_discussions(self, owner: str, repo: str, first: int = 20, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Get repository discussions using GraphQL.
        
        Args:
            owner: Repository owner
            repo: Repository name
            first: Number of discussions to fetch (max 100)
            category: Optional category filter (e.g., "GENERAL", "Q_AND_A", "IDEAS", "PULL_REQUESTS", "ANNOUNCEMENTS")
            
        Returns:
            Repository discussions with comments and reactions
        """
        query = """
        query($owner: String!, $repo: String!, $first: Int!, $category: DiscussionCategory) {
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
                            login
                            name
                            avatarUrl
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
                                login
                                name
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
                                    login
                                    name
                                    avatarUrl
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
        
        return await self.graphql_query(query, variables)
    
    async def get_discussion_categories(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get available discussion categories for a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Available discussion categories
        """
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
        
        return await self.graphql_query(query, variables)
    
    async def get_discussion_by_number(self, owner: str, repo: str, number: int) -> Dict[str, Any]:
        """
        Get a specific discussion by number.
        
        Args:
            owner: Repository owner
            repo: Repository name
            number: Discussion number
            
        Returns:
            Discussion details with all comments and reactions
        """
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
                        login
                        name
                        avatarUrl
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
                            login
                            name
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
                                login
                                name
                                avatarUrl
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
        
        return await self.graphql_query(query, variables)
    
    async def search_discussions(self, query: str, first: int = 20) -> Dict[str, Any]:
        """
        Search discussions across repositories using GraphQL.
        
        Args:
            query: Search query (e.g., "discussions:>0 language:python")
            first: Number of results to return (max 100)
            
        Returns:
            Search results with discussion details
        """
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
                            login
                            name
                            avatarUrl
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
        
        return await self.graphql_query(graphql_query, variables)
