"""
GitHub Smart Authentication Schemas

Pydantic models for GitHub smart authentication API responses.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class GitHubAppInfo(BaseModel):
    """GitHub App information response"""
    success: bool
    app_info: Optional[Dict[str, Any]] = None
    message: str
    error: Optional[str] = None


class GitHubInstallation(BaseModel):
    """GitHub App installation"""
    id: int
    account: Dict[str, Any]
    repository_selection: str
    access_tokens_url: str
    repositories_url: str
    html_url: str
    app_id: int
    app_slug: str
    target_id: int
    target_type: str
    permissions: Dict[str, str]
    events: List[str]
    created_at: str
    updated_at: str
    single_file_name: Optional[str] = None
    has_multiple_single_files: Optional[bool] = None
    single_file_paths: Optional[List[str]] = None
    suspended_by: Optional[Dict[str, Any]] = None
    suspended_at: Optional[str] = None


class GitHubInstallationsResponse(BaseModel):
    """Response for getting all installations"""
    success: bool
    count: int
    installations: List[GitHubInstallation]


class GitHubRepository(BaseModel):
    """GitHub repository"""
    id: int
    node_id: str
    name: str
    full_name: str
    owner: Dict[str, Any]
    private: bool
    html_url: str
    description: Optional[str] = None
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: Optional[str] = None
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: Optional[str] = None
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str] = None
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: Optional[str] = None
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[Dict[str, Any]] = None
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: List[str]
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    installation_id: Optional[int] = None


class GitHubRepositoriesResponse(BaseModel):
    """Response for getting repositories"""
    success: bool
    count: int
    repositories: List[GitHubRepository]


class GitHubRepositoryResponse(BaseModel):
    """Response for getting a single repository"""
    success: bool
    repository: GitHubRepository


class GitHubContentsResponse(BaseModel):
    """Response for getting repository contents"""
    success: bool
    path: str
    contents: List[Dict[str, Any]]


class GitHubFileResponse(BaseModel):
    """Response for getting file content"""
    success: bool
    file: Dict[str, Any]


class GitHubBranch(BaseModel):
    """GitHub branch"""
    name: str
    commit: Dict[str, Any]
    protected: bool


class GitHubBranchesResponse(BaseModel):
    """Response for getting branches"""
    success: bool
    branches: List[GitHubBranch]


class GitHubCommit(BaseModel):
    """GitHub commit"""
    sha: str
    node_id: str
    commit: Dict[str, Any]
    url: str
    html_url: str
    comments_url: str
    author: Optional[Dict[str, Any]] = None
    committer: Optional[Dict[str, Any]] = None
    parents: List[Dict[str, Any]]


class GitHubCommitsResponse(BaseModel):
    """Response for getting commits"""
    success: bool
    branch: str
    commits: List[GitHubCommit]


class GitHubIssue(BaseModel):
    """GitHub issue"""
    id: int
    node_id: str
    url: str
    repository_url: str
    labels_url: str
    comments_url: str
    events_url: str
    html_url: str
    number: int
    state: str
    title: str
    body: Optional[str] = None
    user: Dict[str, Any]
    labels: List[Dict[str, Any]]
    assignee: Optional[Dict[str, Any]] = None
    assignees: List[Dict[str, Any]]
    milestone: Optional[Dict[str, Any]] = None
    locked: bool
    active_lock_reason: Optional[str] = None
    comments: int
    pull_request: Optional[Dict[str, Any]] = None
    closed_at: Optional[str] = None
    created_at: str
    updated_at: str
    author_association: str
    state_reason: Optional[str] = None


class GitHubIssuesResponse(BaseModel):
    """Response for getting issues"""
    success: bool
    state: str
    issues: List[GitHubIssue]


class CreateIssueRequest(BaseModel):
    """Request for creating an issue"""
    title: str
    body: str
    labels: Optional[List[str]] = None


class GitHubIssueResponse(BaseModel):
    """Response for creating an issue"""
    success: bool
    issue: GitHubIssue


class GitHubWebhookResponse(BaseModel):
    """Response for webhook processing"""
    success: bool
    event_type: str
    installation_id: int
    message: str
