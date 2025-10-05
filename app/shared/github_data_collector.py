"""
GitHub Data Collector Service
Fetches all available data from GitHub (REST & GraphQL) for a repository
and stores it in the database.
"""

from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import httpx
from sqlalchemy.orm import Session
from app.core.config import settings
from app.shared.models import (
    Maintainer, Repository, Issue, PullRequest, PRReview, PRReviewComment,
    IssueComment, IssueTimelineEvent, Discussion, DiscussionComment, Commit
)


class GitHubDataCollector:
    """
    Comprehensive GitHub data collector for maintainer dashboard.
    Fetches data from both REST API and GraphQL API.
    """

    def __init__(self, token: Optional[str] = None, use_smart_auth: bool = True):
        self.token = token or settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.graphql_url = "https://api.github.com/graphql"
        self.use_smart_auth = use_smart_auth
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.token}" if self.token else ""
        }
        
        # Import smart auth service if needed
        if use_smart_auth:
            try:
                from app.shared.smart_github_auth import smart_github_auth_service
                self.smart_auth = smart_github_auth_service
            except:
                self.use_smart_auth = False
                self.smart_auth = None

    async def _rest_request(self, method: str, endpoint: str, owner: str = None, repo: str = None, **kwargs) -> Any:
        """Make REST API request to GitHub."""
        headers = self.headers.copy()
        
        # Use smart auth if available and owner/repo provided
        if self.use_smart_auth and self.smart_auth and owner and repo:
            try:
                smart_headers = self.smart_auth.smart_authenticate({'owner': owner, 'repo': repo})
                headers.update(smart_headers)
            except:
                pass  # Fall back to default headers
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/{endpoint}"
            response = await client.request(
                method,
                url,
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def _graphql_request(self, query: str, variables: Optional[Dict] = None, owner: str = None, repo: str = None) -> Dict:
        """Make GraphQL API request to GitHub."""
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        
        # Use smart auth if available and owner/repo provided
        if self.use_smart_auth and self.smart_auth and owner and repo:
            try:
                smart_headers = self.smart_auth.smart_authenticate({'owner': owner, 'repo': repo})
                headers.update(smart_headers)
            except:
                pass  # Fall back to default headers
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.graphql_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    def _get_or_create_maintainer(self, db: Session, user_data: Dict) -> Maintainer:
        """Get or create a maintainer from GitHub user data."""
        if not user_data:
            return None

        github_id = user_data.get('id')
        if not github_id:
            return None

        maintainer = db.query(Maintainer).filter(Maintainer.github_id == github_id).first()
        if not maintainer:
            maintainer = Maintainer(
                github_id=github_id,
                username=user_data.get('login'),
                name=user_data.get('name'),
                email=user_data.get('email'),
                bio=user_data.get('bio'),
                company=user_data.get('company'),
                location=user_data.get('location'),
                blog=user_data.get('blog'),
                avatar_url=user_data.get('avatar_url'),
                html_url=user_data.get('html_url'),
                public_repos=user_data.get('public_repos', 0),
                followers=user_data.get('followers', 0),
                following=user_data.get('following', 0),
                hireable=user_data.get('hireable'),
                created_at=datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00')) if user_data.get('created_at') else None,
                updated_at=datetime.fromisoformat(user_data['updated_at'].replace('Z', '+00:00')) if user_data.get('updated_at') else None,
            )
            db.add(maintainer)
            db.commit()
            db.refresh(maintainer)
        return maintainer

    async def collect_repository_data(
        self, 
        db: Session, 
        owner: str, 
        repo: str, 
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Collect all available GitHub data for a repository for the last N days.
        
        Args:
            db: Database session
            owner: Repository owner
            repo: Repository name
            days: Number of days to look back (default: 30)
            
        Returns:
            Dictionary with collection statistics
        """
        since = datetime.utcnow() - timedelta(days=days)
        since_iso = since.isoformat() + "Z"
        
        stats = {
            "repository": None,
            "maintainers": 0,
            "issues": 0,
            "pull_requests": 0,
            "pr_reviews": 0,
            "pr_review_comments": 0,
            "issue_comments": 0,
            "issue_timeline_events": 0,
            "discussions": 0,
            "discussion_comments": 0,
            "commits": 0,
            "errors": []
        }

        try:
            # 1. Fetch and store repository
            print(f"📦 Fetching repository: {owner}/{repo}")
            repo_data = await self._rest_request("GET", f"repos/{owner}/{repo}", owner=owner, repo=repo)
            repository = await self._store_repository(db, repo_data)
            stats["repository"] = repository.id
            print(f"✅ Repository stored: {repository.full_name}")

            # 2. Fetch and store issues (last 30 days)
            print(f"🐛 Fetching issues...")
            try:
                issues_data = await self._fetch_issues(owner, repo, since_iso)
                print(f"   Found {len(issues_data)} issues to process")
                for issue_data in issues_data:
                    try:
                        await self._store_issue(db, repository.id, issue_data)
                        stats["issues"] += 1
                    except Exception as e:
                        error_msg = f"Failed to store issue #{issue_data.get('number', 'unknown')}: {str(e)}"
                        print(f"   ⚠️  {error_msg}")
                        stats["errors"].append(error_msg)
                print(f"✅ Stored {stats['issues']} issues")
            except Exception as e:
                error_msg = f"Failed to fetch issues: {str(e)}"
                print(f"❌ {error_msg}")
                stats["errors"].append(error_msg)
                import traceback
                traceback.print_exc()

            # 3. Fetch and store pull requests (last 30 days)
            print(f"🔀 Fetching pull requests...")
            try:
                prs_data = await self._fetch_pull_requests(owner, repo, since_iso)
                print(f"   Found {len(prs_data)} pull requests to process")
                for pr_data in prs_data:
                    try:
                        pr = await self._store_pull_request(db, repository.id, pr_data)
                        stats["pull_requests"] += 1
                        
                        # Fetch PR reviews
                        try:
                            reviews = await self._fetch_pr_reviews(owner, repo, pr_data['number'])
                            for review_data in reviews:
                                try:
                                    await self._store_pr_review(db, pr.id, review_data)
                                    stats["pr_reviews"] += 1
                                except Exception as e:
                                    error_msg = f"Failed to store review for PR #{pr_data['number']}: {str(e)}"
                                    print(f"   ⚠️  {error_msg}")
                                    stats["errors"].append(error_msg)
                        except Exception as e:
                            error_msg = f"Failed to fetch reviews for PR #{pr_data['number']}: {str(e)}"
                            print(f"   ⚠️  {error_msg}")
                            stats["errors"].append(error_msg)
                        
                        # Fetch PR review comments
                        try:
                            review_comments = await self._fetch_pr_review_comments(owner, repo, pr_data['number'])
                            for comment_data in review_comments:
                                try:
                                    await self._store_pr_review_comment(db, pr.id, comment_data)
                                    stats["pr_review_comments"] += 1
                                except Exception as e:
                                    error_msg = f"Failed to store review comment for PR #{pr_data['number']}: {str(e)}"
                                    print(f"   ⚠️  {error_msg}")
                                    stats["errors"].append(error_msg)
                        except Exception as e:
                            error_msg = f"Failed to fetch review comments for PR #{pr_data['number']}: {str(e)}"
                            print(f"   ⚠️  {error_msg}")
                            stats["errors"].append(error_msg)
                    except Exception as e:
                        error_msg = f"Failed to store PR #{pr_data.get('number', 'unknown')}: {str(e)}"
                        print(f"   ⚠️  {error_msg}")
                        stats["errors"].append(error_msg)
                
                print(f"✅ Stored {stats['pull_requests']} pull requests, {stats['pr_reviews']} reviews, {stats['pr_review_comments']} review comments")
            except Exception as e:
                error_msg = f"Failed to fetch pull requests: {str(e)}"
                print(f"❌ {error_msg}")
                stats["errors"].append(error_msg)
                import traceback
                traceback.print_exc()

            # 4. Fetch issue comments
            print(f"💬 Fetching issue comments...")
            try:
                for issue_data in issues_data:
                    try:
                        issue = db.query(Issue).filter(Issue.github_id == issue_data['id']).first()
                        if issue and issue_data.get('comments', 0) > 0:
                            comments = await self._fetch_issue_comments(owner, repo, issue_data['number'])
                            for comment_data in comments:
                                try:
                                    await self._store_issue_comment(db, issue.id, comment_data)
                                    stats["issue_comments"] += 1
                                except Exception as e:
                                    error_msg = f"Failed to store comment for issue #{issue_data['number']}: {str(e)}"
                                    print(f"   ⚠️  {error_msg}")
                                    stats["errors"].append(error_msg)
                    except Exception as e:
                        error_msg = f"Failed to fetch comments for issue #{issue_data.get('number', 'unknown')}: {str(e)}"
                        print(f"   ⚠️  {error_msg}")
                        stats["errors"].append(error_msg)
                print(f"✅ Stored {stats['issue_comments']} issue comments")
            except Exception as e:
                error_msg = f"Failed to process issue comments: {str(e)}"
                print(f"❌ {error_msg}")
                stats["errors"].append(error_msg)

            # 5. Fetch issue timeline events
            print(f"📅 Fetching issue timeline events...")
            try:
                for issue_data in issues_data:
                    try:
                        issue = db.query(Issue).filter(Issue.github_id == issue_data['id']).first()
                        if issue:
                            timeline = await self._fetch_issue_timeline(owner, repo, issue_data['number'])
                            for event_data in timeline:
                                try:
                                    await self._store_timeline_event(db, issue.id, event_data)
                                    stats["issue_timeline_events"] += 1
                                except Exception as e:
                                    error_msg = f"Failed to store timeline event for issue #{issue_data['number']}: {str(e)}"
                                    print(f"   ⚠️  {error_msg}")
                                    stats["errors"].append(error_msg)
                    except Exception as e:
                        error_msg = f"Failed to fetch timeline for issue #{issue_data.get('number', 'unknown')}: {str(e)}"
                        print(f"   ⚠️  {error_msg}")
                        stats["errors"].append(error_msg)
                print(f"✅ Stored {stats['issue_timeline_events']} timeline events")
            except Exception as e:
                error_msg = f"Failed to process timeline events: {str(e)}"
                print(f"❌ {error_msg}")
                stats["errors"].append(error_msg)

            # 6. Fetch discussions (GraphQL)
            print(f"💭 Fetching discussions...")
            try:
                discussions_data = await self._fetch_discussions(owner, repo)
                print(f"   Found {len(discussions_data)} discussions to process")
                for discussion_data in discussions_data:
                    try:
                        discussion = await self._store_discussion(db, repository.id, discussion_data)
                        stats["discussions"] += 1
                        
                        # Store discussion comments
                        for comment_data in discussion_data.get('comments', {}).get('nodes', []):
                            try:
                                await self._store_discussion_comment(db, discussion.id, comment_data)
                                stats["discussion_comments"] += 1
                            except Exception as e:
                                error_msg = f"Failed to store discussion comment: {str(e)}"
                                print(f"   ⚠️  {error_msg}")
                                stats["errors"].append(error_msg)
                    except Exception as e:
                        error_msg = f"Failed to store discussion: {str(e)}"
                        print(f"   ⚠️  {error_msg}")
                        stats["errors"].append(error_msg)
                print(f"✅ Stored {stats['discussions']} discussions, {stats['discussion_comments']} discussion comments")
            except Exception as e:
                error_msg = f"Failed to fetch discussions: {str(e)}"
                print(f"❌ {error_msg}")
                stats["errors"].append(error_msg)
                import traceback
                traceback.print_exc()

            # 7. Fetch commits (last 30 days)
            print(f"📝 Fetching commits...")
            try:
                commits_data = await self._fetch_commits(owner, repo, since_iso)
                print(f"   Found {len(commits_data)} commits to process")
                for commit_data in commits_data:
                    try:
                        await self._store_commit(db, repository.id, commit_data)
                        stats["commits"] += 1
                    except Exception as e:
                        error_msg = f"Failed to store commit {commit_data.get('sha', 'unknown')}: {str(e)}"
                        print(f"   ⚠️  {error_msg}")
                        stats["errors"].append(error_msg)
                print(f"✅ Stored {stats['commits']} commits")
            except Exception as e:
                error_msg = f"Failed to fetch commits: {str(e)}"
                print(f"❌ {error_msg}")
                stats["errors"].append(error_msg)
                import traceback
                traceback.print_exc()

            # Count unique maintainers
            stats["maintainers"] = db.query(Maintainer).count()

            print(f"\n🎉 Data collection complete!")
            return stats

        except Exception as e:
            print(f"❌ Error during data collection: {str(e)}")
            stats["errors"].append(str(e))
            raise

    async def _store_repository(self, db: Session, repo_data: Dict) -> Repository:
        """Store repository data."""
        owner_data = repo_data.get('owner', {})
        owner = self._get_or_create_maintainer(db, owner_data)
        
        repository = db.query(Repository).filter(Repository.github_id == repo_data['id']).first()
        if not repository:
            repository = Repository(
                github_id=repo_data['id'],
                owner_id=owner.id if owner else None,
                name=repo_data['name'],
                full_name=repo_data['full_name'],
                description=repo_data.get('description'),
                html_url=repo_data.get('html_url'),
                language=repo_data.get('language'),
                stars=repo_data.get('stargazers_count', 0),
                forks=repo_data.get('forks_count', 0),
                watchers=repo_data.get('watchers_count', 0),
                open_issues=repo_data.get('open_issues_count', 0),
                default_branch=repo_data.get('default_branch', 'main'),
                archived=repo_data.get('archived', False),
                disabled=repo_data.get('disabled', False),
                private=repo_data.get('private', False),
                created_at=datetime.fromisoformat(repo_data['created_at'].replace('Z', '+00:00')) if repo_data.get('created_at') else None,
                updated_at=datetime.fromisoformat(repo_data['updated_at'].replace('Z', '+00:00')) if repo_data.get('updated_at') else None,
                pushed_at=datetime.fromisoformat(repo_data['pushed_at'].replace('Z', '+00:00')) if repo_data.get('pushed_at') else None,
            )
            db.add(repository)
            db.commit()
            db.refresh(repository)
        return repository

    async def _fetch_issues(self, owner: str, repo: str, since: str) -> List[Dict]:
        """Fetch issues created since date with pagination."""
        try:
            all_issues = []
            page = 1
            per_page = 100
            
            while True:
                params = {"state": "all", "since": since, "per_page": per_page, "page": page}
                issues = await self._rest_request("GET", f"repos/{owner}/{repo}/issues", owner=owner, repo=repo, params=params)
                
                if not issues:
                    break
                
                all_issues.extend(issues)
                
                if len(issues) < per_page:
                    break
                
                page += 1
                if page > 50:
                    break
            
            return all_issues
        except Exception as e:
            print(f"Error fetching issues: {e}")
            return []

    async def _store_issue(self, db: Session, repository_id: int, issue_data: Dict) -> Issue:
        """Store issue data."""
        # Skip pull requests (they come through issues endpoint too)
        if 'pull_request' in issue_data:
            return None
            
        issue = db.query(Issue).filter(Issue.github_id == issue_data['id']).first()
        if issue:
            return issue
            
        creator = self._get_or_create_maintainer(db, issue_data.get('user'))
        assignee = self._get_or_create_maintainer(db, issue_data.get('assignee')) if issue_data.get('assignee') else None
        closed_by_user = self._get_or_create_maintainer(db, issue_data.get('closed_by')) if issue_data.get('closed_by') else None
        
        issue = Issue(
            github_id=issue_data['id'],
            repository_id=repository_id,
            number=issue_data['number'],
            title=issue_data['title'],
            body=issue_data.get('body'),
            state=issue_data['state'],
            created_by=creator.id if creator else None,
            assigned_to=assignee.id if assignee else None,
            closed_by=closed_by_user.id if closed_by_user else None,
            labels=[label['name'] for label in issue_data.get('labels', [])],
            comments_count=issue_data.get('comments', 0),
            html_url=issue_data.get('html_url'),
            created_at=datetime.fromisoformat(issue_data['created_at'].replace('Z', '+00:00')) if issue_data.get('created_at') else None,
            updated_at=datetime.fromisoformat(issue_data['updated_at'].replace('Z', '+00:00')) if issue_data.get('updated_at') else None,
            closed_at=datetime.fromisoformat(issue_data['closed_at'].replace('Z', '+00:00')) if issue_data.get('closed_at') else None,
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return issue

    async def _fetch_pull_requests(self, owner: str, repo: str, since: str) -> List[Dict]:
        """Fetch pull requests created since date with pagination."""
        try:
            all_prs = []
            page = 1
            per_page = 100
            since_dt = datetime.fromisoformat(since.replace('Z', '+00:00'))
            
            while True:
                params = {"state": "all", "per_page": per_page, "page": page, "sort": "created", "direction": "desc"}
                prs = await self._rest_request("GET", f"repos/{owner}/{repo}/pulls", owner=owner, repo=repo, params=params)
                
                if not prs:
                    break
                
                # Filter by date and add to results
                filtered_prs = [pr for pr in prs if datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00')) >= since_dt]
                all_prs.extend(filtered_prs)
                
                # If we got PRs older than since_dt, we can stop
                if len(filtered_prs) < len(prs):
                    break
                
                if len(prs) < per_page:
                    break
                
                page += 1
                if page > 50:
                    break
            
            return all_prs
        except Exception as e:
            print(f"Error fetching pull requests: {e}")
            return []

    async def _store_pull_request(self, db: Session, repository_id: int, pr_data: Dict) -> PullRequest:
        """Store pull request data."""
        pr = db.query(PullRequest).filter(PullRequest.github_id == pr_data['id']).first()
        if pr:
            return pr
            
        creator = self._get_or_create_maintainer(db, pr_data.get('user'))
        merged_by_user = self._get_or_create_maintainer(db, pr_data.get('merged_by')) if pr_data.get('merged_by') else None
        
        pr = PullRequest(
            github_id=pr_data['id'],
            repository_id=repository_id,
            number=pr_data['number'],
            title=pr_data['title'],
            body=pr_data.get('body'),
            state=pr_data['state'],
            created_by=creator.id if creator else None,
            merged_by=merged_by_user.id if merged_by_user else None,
            commits_count=pr_data.get('commits', 0),
            additions=pr_data.get('additions', 0),
            deletions=pr_data.get('deletions', 0),
            changed_files=pr_data.get('changed_files', 0),
            review_comments_count=pr_data.get('review_comments', 0),
            comments_count=pr_data.get('comments', 0),
            draft=pr_data.get('draft', False),
            merged=pr_data.get('merged', False),
            html_url=pr_data.get('html_url'),
            created_at=datetime.fromisoformat(pr_data['created_at'].replace('Z', '+00:00')) if pr_data.get('created_at') else None,
            updated_at=datetime.fromisoformat(pr_data['updated_at'].replace('Z', '+00:00')) if pr_data.get('updated_at') else None,
            closed_at=datetime.fromisoformat(pr_data['closed_at'].replace('Z', '+00:00')) if pr_data.get('closed_at') else None,
            merged_at=datetime.fromisoformat(pr_data['merged_at'].replace('Z', '+00:00')) if pr_data.get('merged_at') else None,
        )
        db.add(pr)
        db.commit()
        db.refresh(pr)
        return pr

    async def _fetch_pr_reviews(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """Fetch PR reviews."""
        try:
            return await self._rest_request("GET", f"repos/{owner}/{repo}/pulls/{pr_number}/reviews", owner=owner, repo=repo)
        except Exception as e:
            print(f"Error fetching PR reviews for #{pr_number}: {e}")
            return []

    async def _store_pr_review(self, db: Session, pr_id: int, review_data: Dict) -> PRReview:
        """Store PR review data."""
        review = db.query(PRReview).filter(PRReview.github_id == review_data['id']).first()
        if review:
            return review
            
        reviewer = self._get_or_create_maintainer(db, review_data.get('user'))
        
        review = PRReview(
            github_id=review_data['id'],
            pull_request_id=pr_id,
            reviewer_id=reviewer.id if reviewer else None,
            state=review_data['state'],
            body=review_data.get('body'),
            commit_id=review_data.get('commit_id'),
            html_url=review_data.get('html_url'),
            submitted_at=datetime.fromisoformat(review_data['submitted_at'].replace('Z', '+00:00')) if review_data.get('submitted_at') else None,
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    async def _fetch_pr_review_comments(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """Fetch PR review comments (inline comments)."""
        try:
            return await self._rest_request("GET", f"repos/{owner}/{repo}/pulls/{pr_number}/comments", owner=owner, repo=repo)
        except Exception as e:
            print(f"Error fetching PR review comments for #{pr_number}: {e}")
            return []

    async def _store_pr_review_comment(self, db: Session, pr_id: int, comment_data: Dict) -> PRReviewComment:
        """Store PR review comment data."""
        comment = db.query(PRReviewComment).filter(PRReviewComment.github_id == comment_data['id']).first()
        if comment:
            return comment
            
        commenter = self._get_or_create_maintainer(db, comment_data.get('user'))
        
        comment = PRReviewComment(
            github_id=comment_data['id'],
            pull_request_id=pr_id,
            review_id=None,  # Will be linked later if needed
            commenter_id=commenter.id if commenter else None,
            body=comment_data['body'],
            path=comment_data.get('path'),
            position=comment_data.get('position'),
            line=comment_data.get('line'),
            in_reply_to_id=comment_data.get('in_reply_to_id'),
            html_url=comment_data.get('html_url'),
            created_at=datetime.fromisoformat(comment_data['created_at'].replace('Z', '+00:00')) if comment_data.get('created_at') else None,
            updated_at=datetime.fromisoformat(comment_data['updated_at'].replace('Z', '+00:00')) if comment_data.get('updated_at') else None,
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    async def _fetch_issue_comments(self, owner: str, repo: str, issue_number: int) -> List[Dict]:
        """Fetch issue comments."""
        try:
            return await self._rest_request("GET", f"repos/{owner}/{repo}/issues/{issue_number}/comments", owner=owner, repo=repo)
        except Exception as e:
            print(f"Error fetching issue comments for #{issue_number}: {e}")
            return []

    async def _store_issue_comment(self, db: Session, issue_id: int, comment_data: Dict) -> IssueComment:
        """Store issue comment data."""
        comment = db.query(IssueComment).filter(IssueComment.github_id == comment_data['id']).first()
        if comment:
            return comment
            
        commenter = self._get_or_create_maintainer(db, comment_data.get('user'))
        
        # Parse reactions
        reactions = {}
        if 'reactions' in comment_data:
            reactions = {
                'heart': comment_data['reactions'].get('heart', 0),
                '+1': comment_data['reactions'].get('+1', 0),
                '-1': comment_data['reactions'].get('-1', 0),
                'laugh': comment_data['reactions'].get('laugh', 0),
                'hooray': comment_data['reactions'].get('hooray', 0),
                'confused': comment_data['reactions'].get('confused', 0),
                'rocket': comment_data['reactions'].get('rocket', 0),
                'eyes': comment_data['reactions'].get('eyes', 0),
            }
        
        comment = IssueComment(
            github_id=comment_data['id'],
            issue_id=issue_id,
            commenter_id=commenter.id if commenter else None,
            body=comment_data['body'],
            reactions=reactions,
            html_url=comment_data.get('html_url'),
            created_at=datetime.fromisoformat(comment_data['created_at'].replace('Z', '+00:00')) if comment_data.get('created_at') else None,
            updated_at=datetime.fromisoformat(comment_data['updated_at'].replace('Z', '+00:00')) if comment_data.get('updated_at') else None,
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    async def _fetch_issue_timeline(self, owner: str, repo: str, issue_number: int) -> List[Dict]:
        """Fetch issue timeline events."""
        try:
            headers = {**self.headers, "Accept": "application/vnd.github.mockingbird-preview+json"}
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/timeline"
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching timeline for issue #{issue_number}: {e}")
            return []

    async def _store_timeline_event(self, db: Session, issue_id: int, event_data: Dict) -> IssueTimelineEvent:
        """Store issue timeline event."""
        event_id = event_data.get('id')
        if event_id:
            event = db.query(IssueTimelineEvent).filter(IssueTimelineEvent.github_id == event_id).first()
            if event:
                return event
        
        actor = self._get_or_create_maintainer(db, event_data.get('actor'))
        assignee = self._get_or_create_maintainer(db, event_data.get('assignee')) if event_data.get('assignee') else None
        
        event = IssueTimelineEvent(
            github_id=event_id,
            issue_id=issue_id,
            event_type=event_data.get('event', ''),
            actor_id=actor.id if actor else None,
            label_name=event_data.get('label', {}).get('name') if event_data.get('label') else None,
            assignee_id=assignee.id if assignee else None,
            created_at=datetime.fromisoformat(event_data['created_at'].replace('Z', '+00:00')) if event_data.get('created_at') else None,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    async def _fetch_discussions(self, owner: str, repo: str) -> List[Dict]:
        """Fetch discussions using GraphQL."""
        try:
            query = """
            query($owner: String!, $repo: String!) {
                repository(owner: $owner, name: $repo) {
                    discussions(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                        nodes {
                            id
                            number
                            title
                            body
                            createdAt
                            updatedAt
                            author {
                                login
                                ... on User {
                                    id
                                    name
                                    email
                                    bio
                                    company
                                    location
                                    avatarUrl
                                    url
                                }
                            }
                            category {
                                name
                            }
                            answer {
                                author {
                                    login
                                }
                            }
                            comments(first: 100) {
                                nodes {
                                    id
                                    body
                                    createdAt
                                    updatedAt
                                    isAnswer
                                    upvoteCount
                                    author {
                                        login
                                        ... on User {
                                            id
                                            name
                                            email
                                            avatarUrl
                                            url
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """
            variables = {"owner": owner, "repo": repo}
            result = await self._graphql_request(query, variables, owner=owner, repo=repo)
            discussions = result.get('data', {}).get('repository', {}).get('discussions', {}).get('nodes', [])
            print(f"   GraphQL returned {len(discussions)} discussions")
            return discussions
        except Exception as e:
            print(f"❌ Error fetching discussions: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def _store_discussion(self, db: Session, repository_id: int, discussion_data: Dict) -> Discussion:
        """Store discussion data."""
        discussion = db.query(Discussion).filter(Discussion.github_id == discussion_data['id']).first()
        if discussion:
            return discussion
            
        author = self._get_or_create_maintainer(db, discussion_data.get('author'))
        answered_by_user = None
        if discussion_data.get('answer'):
            answered_by_user = self._get_or_create_maintainer(db, discussion_data['answer'].get('author'))
        
        discussion = Discussion(
            github_id=discussion_data['id'],
            repository_id=repository_id,
            number=discussion_data['number'],
            title=discussion_data['title'],
            body=discussion_data.get('body'),
            category=discussion_data.get('category', {}).get('name'),
            author_id=author.id if author else None,
            is_answered=discussion_data.get('answer') is not None,
            answered_by=answered_by_user.id if answered_by_user else None,
            created_at=datetime.fromisoformat(discussion_data['createdAt'].replace('Z', '+00:00')) if discussion_data.get('createdAt') else None,
            updated_at=datetime.fromisoformat(discussion_data['updatedAt'].replace('Z', '+00:00')) if discussion_data.get('updatedAt') else None,
        )
        db.add(discussion)
        db.commit()
        db.refresh(discussion)
        return discussion

    async def _store_discussion_comment(self, db: Session, discussion_id: int, comment_data: Dict) -> DiscussionComment:
        """Store discussion comment data."""
        comment = db.query(DiscussionComment).filter(DiscussionComment.github_id == comment_data['id']).first()
        if comment:
            return comment
            
        commenter = self._get_or_create_maintainer(db, comment_data.get('author'))
        
        comment = DiscussionComment(
            github_id=comment_data['id'],
            discussion_id=discussion_id,
            commenter_id=commenter.id if commenter else None,
            body=comment_data['body'],
            is_answer=comment_data.get('isAnswer', False),
            upvotes=comment_data.get('upvoteCount', 0),
            created_at=datetime.fromisoformat(comment_data['createdAt'].replace('Z', '+00:00')) if comment_data.get('createdAt') else None,
            updated_at=datetime.fromisoformat(comment_data['updatedAt'].replace('Z', '+00:00')) if comment_data.get('updatedAt') else None,
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    async def _fetch_commits(self, owner: str, repo: str, since: str) -> List[Dict]:
        """Fetch commits since date with pagination."""
        try:
            all_commits = []
            page = 1
            per_page = 100
            
            while True:
                params = {"since": since, "per_page": per_page, "page": page}
                commits = await self._rest_request("GET", f"repos/{owner}/{repo}/commits", owner=owner, repo=repo, params=params)
                
                if not commits:
                    break
                
                all_commits.extend(commits)
                print(f"  Fetched page {page}: {len(commits)} commits")
                
                # If we got fewer than per_page commits, we've reached the end
                if len(commits) < per_page:
                    break
                
                page += 1
                
                # Safety check
                if page > 50:
                    print(f"  Warning: Reached max pages (50) for commits")
                    break
            
            print(f"  Total commits fetched: {len(all_commits)}")
            return all_commits
        except Exception as e:
            print(f"Error fetching commits: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def _store_commit(self, db: Session, repository_id: int, commit_data: Dict) -> Commit:
        """Store commit data."""
        sha = commit_data['sha']
        commit = db.query(Commit).filter(Commit.sha == sha).first()
        if commit:
            return commit
        
        # Try to match author by email
        author_email = commit_data.get('commit', {}).get('author', {}).get('email')
        author = None
        if author_email:
            author = db.query(Maintainer).filter(Maintainer.email == author_email).first()
        
        commit = Commit(
            sha=sha,
            repository_id=repository_id,
            author_id=author.id if author else None,
            author_name=commit_data.get('commit', {}).get('author', {}).get('name'),
            author_email=author_email,
            message=commit_data.get('commit', {}).get('message'),
            additions=commit_data.get('stats', {}).get('additions', 0),
            deletions=commit_data.get('stats', {}).get('deletions', 0),
            changed_files=len(commit_data.get('files', [])),
            html_url=commit_data.get('html_url'),
            created_at=datetime.fromisoformat(commit_data['commit']['author']['date'].replace('Z', '+00:00')) if commit_data.get('commit', {}).get('author', {}).get('date') else None,
        )
        db.add(commit)
        db.commit()
        db.refresh(commit)
        return commit

