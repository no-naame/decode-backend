from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Maintainer(Base):
    """
    GitHub users who are contributors/maintainers.
    Maps to GitHub API: /users/{username}
    """
    __tablename__ = "maintainers"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    blog = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    html_url = Column(String, nullable=True)
    public_repos = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    hireable = Column(Boolean, nullable=True)
    is_active = Column(Boolean, default=True)
    last_activity_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)  # GitHub account creation
    updated_at = Column(DateTime, nullable=True)  # GitHub account update
    fetched_at = Column(DateTime, default=datetime.utcnow)  # When we fetched this data


class Repository(Base):
    """
    Project repositories maintained by users.
    Maps to GitHub API: /repos/{owner}/{repo}
    """
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    name = Column(String, nullable=False)
    full_name = Column(String, unique=True, index=True, nullable=False)  # owner/repo
    description = Column(Text, nullable=True)
    html_url = Column(String, nullable=True)
    language = Column(String, nullable=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    watchers = Column(Integer, default=0)
    open_issues = Column(Integer, default=0)
    default_branch = Column(String, default="main")
    archived = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    private = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=True)  # GitHub repo creation
    updated_at = Column(DateTime, nullable=True)  # GitHub repo update
    pushed_at = Column(DateTime, nullable=True)  # Last push
    fetched_at = Column(DateTime, default=datetime.utcnow)


class Issue(Base):
    """
    Issues in repositories (bugs, features, questions).
    Maps to GitHub API: /repos/{owner}/{repo}/issues/{issue_number}
    """
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=True)
    state = Column(String, nullable=False)  # 'open' or 'closed'
    created_by = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    assigned_to = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    closed_by = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    labels = Column(JSON, nullable=True)  # Array of label names
    comments_count = Column(Integer, default=0)
    html_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class PullRequest(Base):
    """
    Pull requests for code changes.
    Maps to GitHub API: /repos/{owner}/{repo}/pulls/{pull_number}
    """
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=True)
    state = Column(String, nullable=False)  # 'open', 'closed', 'merged'
    created_by = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    merged_by = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    commits_count = Column(Integer, default=0)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    changed_files = Column(Integer, default=0)
    review_comments_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    draft = Column(Boolean, default=False)
    merged = Column(Boolean, default=False)
    html_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    merged_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class PRReview(Base):
    """
    Pull request reviews showing maintainer review activity.
    Maps to GitHub API: /repos/{owner}/{repo}/pulls/{pull_number}/reviews
    """
    __tablename__ = "pr_reviews"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
    pull_request_id = Column(Integer, ForeignKey('pull_requests.id'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    state = Column(String, nullable=False)  # 'APPROVED', 'CHANGES_REQUESTED', 'COMMENTED', 'DISMISSED', 'PENDING'
    body = Column(Text, nullable=True)
    commit_id = Column(String, nullable=True)
    html_url = Column(String, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    # Custom metrics - to be calculated later
    review_depth_score = Column(Float, nullable=True)
    lines_reviewed = Column(Integer, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class PRReviewComment(Base):
    """
    Individual inline comments on PR diffs (mentorship activity).
    Maps to GitHub API: /repos/{owner}/{repo}/pulls/{pull_number}/comments
    """
    __tablename__ = "pr_review_comments"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
    pull_request_id = Column(Integer, ForeignKey('pull_requests.id'), nullable=False)
    review_id = Column(Integer, ForeignKey('pr_reviews.id'), nullable=True)
    commenter_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    body = Column(Text, nullable=False)
    path = Column(String, nullable=True)  # File being commented on
    position = Column(Integer, nullable=True)  # Position in diff
    line = Column(Integer, nullable=True)  # Line number
    in_reply_to_id = Column(BigInteger, nullable=True)  # Thread conversation
    html_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class IssueComment(Base):
    """
    Comments on issues (community engagement).
    Maps to GitHub API: /repos/{owner}/{repo}/issues/{issue_number}/comments
    """
    __tablename__ = "issue_comments"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
    issue_id = Column(Integer, ForeignKey('issues.id'), nullable=False)
    commenter_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    body = Column(Text, nullable=False)
    reactions = Column(JSON, nullable=True)  # {"heart": 5, "+1": 3, etc.}
    html_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class IssueTimelineEvent(Base):
    """
    Triage activities: labeling, assigning, closing issues.
    Maps to GitHub API: /repos/{owner}/{repo}/issues/{issue_number}/timeline
    """
    __tablename__ = "issue_timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=True, index=True)  # Some events don't have IDs
    issue_id = Column(Integer, ForeignKey('issues.id'), nullable=False)
    event_type = Column(String, nullable=False)  # 'labeled', 'unlabeled', 'assigned', 'closed', etc.
    actor_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    label_name = Column(String, nullable=True)
    assignee_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    created_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class Discussion(Base):
    """
    GitHub Discussions for Q&A and community engagement.
    Maps to GitHub GraphQL API: discussion type
    """
    __tablename__ = "discussions"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, nullable=False, index=True)  # GraphQL node ID
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # 'Q&A', 'Ideas', 'Show and tell', etc.
    author_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    is_answered = Column(Boolean, default=False)
    answered_by = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    html_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class DiscussionComment(Base):
    """
    Comments in discussions (mentorship and community support).
    Maps to GitHub GraphQL API: discussionComment type
    """
    __tablename__ = "discussion_comments"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, nullable=False, index=True)  # GraphQL node ID
    discussion_id = Column(Integer, ForeignKey('discussions.id'), nullable=False)
    commenter_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    body = Column(Text, nullable=False)
    parent_comment_id = Column(Integer, ForeignKey('discussion_comments.id'), nullable=True)  # For threaded conversations
    is_answer = Column(Boolean, default=False)
    upvotes = Column(Integer, default=0)
    html_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class Commit(Base):
    """
    Code commits (tracks documentation maintenance).
    Maps to GitHub API: /repos/{owner}/{repo}/commits/{sha}
    """
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    sha = Column(String, unique=True, nullable=False, index=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('maintainers.id'), nullable=True)
    author_name = Column(String, nullable=True)
    author_email = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    changed_files = Column(Integer, default=0)
    html_url = Column(String, nullable=True)
    # Custom flag - to be calculated later
    is_docs_related = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=True)  # Commit date
    fetched_at = Column(DateTime, default=datetime.utcnow)


# Custom analysis tables - to be populated later with calculations

class SentimentAnalysis(Base):
    """
    AI sentiment analysis results for maintainer communications.
    Custom table - to be calculated using Gemini API
    """
    __tablename__ = "sentiment_analysis"

    id = Column(Integer, primary_key=True, index=True)
    maintainer_id = Column(Integer, ForeignKey('maintainers.id'), nullable=False)
    content_type = Column(String, nullable=False)  # 'pr_review', 'issue_comment', 'discussion_comment'
    content_id = Column(Integer, nullable=False)  # ID of the analyzed content
    sentiment_score = Column(Float, nullable=False)  # -1.0 to 1.0
    tone = Column(String, nullable=True)  # 'constructive', 'neutral', 'harsh', 'supportive'
    text_analyzed = Column(Text, nullable=False)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class BurnoutRiskScore(Base):
    """
    Calculated burnout risk indicators.
    Custom table - to be calculated based on activity patterns
    """
    __tablename__ = "burnout_risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    maintainer_id = Column(Integer, ForeignKey('maintainers.id'), nullable=False)
    overall_risk_score = Column(Float, nullable=False)  # 0-100
    response_time_score = Column(Float, nullable=True)
    activity_level_score = Column(Float, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    isolation_score = Column(Float, nullable=True)
    workload_score = Column(Float, nullable=True)
    community_support_score = Column(Float, nullable=True)
    calculation_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


# Legacy models for backward compatibility
class User(Base):
    """Legacy User model - redirects to Maintainer"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    github_id = Column(Integer, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AnalysisCache(Base):
    """
    Cache for expensive analysis results.
    Shared across modules to avoid re-computation.
    """
    __tablename__ = "analysis_cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True, nullable=False)
    module = Column(String, nullable=False)  # which module created this
    data = Column(JSON, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
