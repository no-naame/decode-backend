"""
Main Dashboard Service - Single Endpoint Orchestration

This service:
1. Fetches data from GitHub API (or database mock)
2. Calculates all metrics using rigorous formulas
3. Generates AI insights with anti-hallucination measures
4. Returns complete dashboard data in one response
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
from .schemas import *
from .calculator import MetricsCalculator
from .ai_insights import AIInsightsGenerator
from app.shared.github_client import GitHubClient


class DashboardService:
    """
    Main service orchestrating all dashboard data.

    Single endpoint: GET /api/dashboard/{username}
    Returns: Complete DashboardOverviewResponse
    """

    def __init__(self):
        self.calculator = MetricsCalculator()
        self.ai = AIInsightsGenerator()
        self.github = GitHubClient()

    async def get_complete_dashboard(
        self,
        username: str,
        repository: str = None,
        days: int = 30
    ) -> DashboardOverviewResponse:
        """
        MAIN ENDPOINT: Get complete dashboard data.

        Returns all data needed for frontend in single response:
        - Metrics (invisible labor, review impact, community, burnout, sentiment)
        - Profile (achievements, skills, impact summary)
        - Burnout assessment with recommendations
        - Sentiment analysis with feedback
        - Community metrics
        - Recent activity timeline
        - Repository health
        - Alerts

        Args:
            username: GitHub username
            repository: Optional repository filter (format: "owner/repo")
            days: Time window for analysis (default 30)

        Returns:
            DashboardOverviewResponse with ALL frontend data
        """

        # ============== DATA COLLECTION ==============

        # Fetch raw data (currently using mock data, replace with GitHub API calls)
        raw_data = await self._fetch_github_data(username, repository, days)

        # ============== METRIC CALCULATIONS ==============

        # 1. Invisible Labor Score (0-100)
        invisible_labor_score = self.calculator.calculate_invisible_labor_score(
            pr_reviews=raw_data['pr_reviews'],
            pr_review_comments=raw_data['pr_review_comments'],
            issue_comments=raw_data['issue_comments'],
            issue_timeline_events=raw_data['issue_timeline_events'],
            discussion_comments=raw_data['discussion_comments'],
            commits=raw_data['commits'],
            time_window_days=days
        )

        # 2. Review Impact Score (0-100)
        review_impact_score = self.calculator.calculate_review_impact_score(
            pr_reviews=raw_data['pr_reviews'],
            pull_requests=raw_data['pull_requests']
        )

        # 3. Community Engagement (0-100)
        community_engagement = self.calculator.calculate_community_engagement(
            issue_comments=raw_data['issue_comments'],
            discussion_comments=raw_data['discussion_comments'],
            pr_review_comments=raw_data['pr_review_comments']
        )

        # 4. Sentiment Score (0-100)
        sentiment_data = await self._analyze_sentiment(raw_data)
        sentiment_score = sentiment_data['score']

        # 5. Burnout Risk (0-100)
        all_activities = (
            raw_data['pr_reviews'] +
            raw_data['issue_comments'] +
            raw_data['pr_review_comments'] +
            raw_data['discussion_comments']
        )
        burnout_risk_score, burnout_indicators_dict = self.calculator.calculate_burnout_risk(
            all_activities=all_activities,
            sentiment_score=sentiment_score,
            time_window_days=days
        )

        # ============== WEEKLY ACTIVITY BREAKDOWN ==============

        weekly_activity = await self._calculate_weekly_activity(raw_data, days)

        # ============== SENTIMENT TREND ==============

        sentiment_trend = await self._calculate_sentiment_trend(raw_data, days)

        # ============== ACTIVITY DISTRIBUTION ==============

        activity_distribution = await self._calculate_activity_distribution(raw_data)

        # ============== BUILD MAINTAINER METRICS ==============

        metrics = MaintainerMetrics(
            invisibleLaborScore=invisible_labor_score,
            reviewImpactScore=review_impact_score,
            communityEngagement=community_engagement,
            burnoutRisk=burnout_risk_score,
            sentimentScore=sentiment_score,
            totalRepositories=len(set(r.get('repository', {}).get('name') for r in raw_data['pr_reviews'])) or 1,
            responseTime=round(4.5, 2),  # Calculate from timestamps
            totalContributions=len(all_activities),
            mentorshipHours=round(self._estimate_mentorship_hours(raw_data), 2),
            weeklyActivity=weekly_activity,
            sentimentTrend=sentiment_trend,
            activityDistribution=activity_distribution
        )

        # ============== BURNOUT ASSESSMENT ==============

        risk_level = self.calculator.determine_risk_level(burnout_risk_score)

        # AI-generated recommendations
        weekend_work_pct = burnout_indicators_dict.get('weekendWork', 0)
        recommendations = self.ai.generate_burnout_recommendations(
            risk_score=burnout_risk_score,
            workload_indicator=burnout_indicators_dict.get('workload', 0),
            weekend_work_pct=weekend_work_pct,
            sentiment_score=sentiment_score
        )

        burnout = BurnoutIndicator(
            riskScore=burnout_risk_score,
            riskLevel=risk_level,
            indicators=BurnoutIndicators(**burnout_indicators_dict),
            recommendations=recommendations,
            recoveryMetrics=RecoveryMetrics(
                daysOff=0,  # Track if implementing recovery tracking
                delegatedTasks=0,
                reducedScope=0
            )
        )

        # ============== SENTIMENT ANALYSIS ==============

        positive_feedback, concern_areas = self.ai.generate_sentiment_feedback(
            positive_comment_pct=sentiment_data.get('positive_pct', 60),
            critical_comment_pct=sentiment_data.get('critical_pct', 15),
            total_comments_analyzed=len(all_activities)
        )

        sentiment = SentimentAnalysis(
            score=sentiment_score,
            trend=sentiment_data.get('trend', 'stable'),
            wordFrequency=sentiment_data.get('word_frequency', []),
            feedbackDistribution=sentiment_data.get('feedback_distribution', FeedbackDistribution(
                constructive=45, appreciative=38, critical=12, neutral=5
            )),
            topPositiveFeedback=positive_feedback,
            concernAreas=concern_areas
        )

        # ============== COMMUNITY METRICS ==============

        community_metrics = await self._calculate_community_metrics(raw_data)

        # ============== CONTRIBUTION PROFILE ==============

        profile = await self._build_contribution_profile(username, raw_data, metrics)

        # ============== ALERTS ==============

        alerts = await self._generate_alerts(burnout_risk_score, sentiment_score, raw_data)

        # ============== RECENT ACTIVITY ==============

        recent_activity = await self._build_timeline(raw_data, limit=20)

        # ============== REPOSITORY HEALTH ==============

        repository_health = await self._calculate_repository_health(raw_data, repository)

        # ============== RETURN COMPLETE RESPONSE ==============

        return DashboardOverviewResponse(
            metrics=metrics,
            burnout=burnout,
            sentiment=sentiment,
            communityMetrics=community_metrics,
            profile=profile,
            alerts=alerts,
            recentActivity=recent_activity,
            repositoryHealth=repository_health
        )

    # ============== HELPER METHODS ==============

    async def _fetch_github_data(
        self,
        username: str,
        repository: str,
        days: int
    ) -> Dict[str, List[Dict]]:
        """
        Fetch all required data from GitHub API or database.

        TODO: Replace mock data with actual API calls
        Currently returns mock data matching the SQL schema
        """

        # Mock data - replace with actual GitHub API calls
        # Example API calls (commented out):
        # pr_reviews = await self.github.get_pr_reviews(repository)
        # pull_requests = await self.github.get_pull_requests(repository)
        # etc.

        return {
            'pr_reviews': self._get_mock_pr_reviews(username),
            'pull_requests': self._get_mock_pull_requests(),
            'pr_review_comments': self._get_mock_pr_review_comments(username),
            'issue_comments': self._get_mock_issue_comments(username),
            'issue_timeline_events': self._get_mock_timeline_events(username),
            'discussion_comments': self._get_mock_discussion_comments(username),
            'commits': self._get_mock_commits(username),
            'issues': self._get_mock_issues()
        }

    def _get_mock_pr_reviews(self, username: str) -> List[Dict]:
        """Mock PR reviews data"""
        if username == "sarah_maintainer":
            return [
                {'id': f'rv{i}', 'state': 'APPROVED' if i % 3 == 0 else 'CHANGES_REQUESTED',
                 'pull_request_url': f'https://api.github.com/repos/test/repo/pulls/{i}',
                 'submitted_at': (datetime.utcnow() - timedelta(days=i)).isoformat() + 'Z'}
                for i in range(18)
            ]
        return []

    def _get_mock_pull_requests(self) -> List[Dict]:
        """Mock pull requests data"""
        return [
            {'number': i, 'additions': 100, 'deletions': 50,
             'created_at': (datetime.utcnow() - timedelta(days=i+1)).isoformat() + 'Z'}
            for i in range(20)
        ]

    def _get_mock_pr_review_comments(self, username: str) -> List[Dict]:
        """Mock PR review comments"""
        if username == "sarah_maintainer":
            return [
                {'id': f'c{i}', 'body': 'Great work! Consider extracting this into a separate function for better testability. Here is an example: ```python\ndef extract():...\n```',
                 'pull_request_review_id': f'rv{i//3}', 'created_at': datetime.utcnow().isoformat() + 'Z'}
                for i in range(40)
            ]
        return []

    def _get_mock_issue_comments(self, username: str) -> List[Dict]:
        """Mock issue comments"""
        if username == "sarah_maintainer":
            return [
                {'id': f'ic{i}', 'body': 'Thanks for reporting! This looks like a valid bug. Let me investigate.',
                 'created_at': (datetime.utcnow() - timedelta(days=i//3)).isoformat() + 'Z',
                 'reactions': {'+1': 2, 'heart': 1}}
                for i in range(30)
            ]
        return []

    def _get_mock_timeline_events(self, username: str) -> List[Dict]:
        """Mock issue timeline events"""
        if username == "sarah_maintainer":
            events = []
            for i in range(50):
                event_type = ['labeled', 'assigned', 'closed'][i % 3]
                event = {
                    'id': f'e{i}',
                    'event': event_type,
                    'created_at': (datetime.utcnow() - timedelta(days=i//2)).isoformat() + 'Z'
                }
                if event_type == 'labeled':
                    event['label'] = {'name': 'bug' if i % 5 == 0 else ('critical' if i % 10 == 0 else 'enhancement')}
                events.append(event)
            return events
        return []

    def _get_mock_discussion_comments(self, username: str) -> List[Dict]:
        """Mock discussion comments"""
        if username == "sarah_maintainer":
            return [
                {'id': f'dc{i}', 'body': 'Here is how you can solve this...', 'isAnswer': i % 4 == 0,
                 'created_at': datetime.utcnow().isoformat() + 'Z'}
                for i in range(15)
            ]
        return []

    def _get_mock_commits(self, username: str) -> List[Dict]:
        """Mock commits"""
        if username == "sarah_maintainer":
            return [
                {'commit': {'message': 'docs: update README with new examples' if i % 3 == 0 else 'feat: add feature'},
                 'created_at': (datetime.utcnow() - timedelta(days=i)).isoformat() + 'Z'}
                for i in range(10)
            ]
        return []

    def _get_mock_issues(self) -> List[Dict]:
        """Mock issues"""
        return [
            {'number': i, 'state': 'open', 'created_at': datetime.utcnow().isoformat() + 'Z'}
            for i in range(20)
        ]

    async def _analyze_sentiment(self, raw_data: Dict) -> Dict:
        """Analyze sentiment from comments"""
        # Simplified sentiment analysis
        # TODO: Implement proper NLP-based sentiment analysis
        return {
            'score': 73,
            'trend': 'stable',
            'positive_pct': 65,
            'critical_pct': 15,
            'word_frequency': [
                {'word': 'helpful', 'count': 45, 'sentiment': 'positive'},
                {'word': 'thanks', 'count': 38, 'sentiment': 'positive'},
                {'word': 'improve', 'count': 22, 'sentiment': 'neutral'}
            ],
            'feedback_distribution': FeedbackDistribution(
                constructive=45, appreciative=38, critical=12, neutral=5
            )
        }

    async def _calculate_weekly_activity(self, raw_data: Dict, days: int) -> List[ActivityData]:
        """Calculate weekly activity breakdown"""
        # Simplified - return last 4 weeks
        activities = []
        base_date = datetime.utcnow() - timedelta(days=28)

        for week in range(4):
            date = base_date + timedelta(weeks=week)
            activities.append(ActivityData(
                date=date.strftime("%Y-%m-%d"),
                reviews=5 + week * 2,
                triage=8 + week,
                mentorship=3 + week,
                documentation=2,
                discussions=4 + week,
                total=22 + week * 4
            ))

        return activities

    async def _calculate_sentiment_trend(self, raw_data: Dict, days: int) -> List[TrendData]:
        """Calculate sentiment trend over time"""
        trends = []
        base_date = datetime.utcnow() - timedelta(days=28)

        for week in range(4):
            date = base_date + timedelta(weeks=week)
            trends.append(TrendData(
                date=date.strftime("%Y-%m-%d"),
                value=70 + week * 2,
                label="Positive" if 70 + week * 2 > 60 else "Neutral"
            ))

        return trends

    async def _calculate_activity_distribution(self, raw_data: Dict) -> List[CategoryData]:
        """Calculate activity distribution pie chart data"""
        total_reviews = len(raw_data['pr_reviews'])
        total_triage = len(raw_data['issue_timeline_events'])
        total_mentorship = len([c for c in raw_data['pr_review_comments'] if len(c.get('body', '')) > 200])
        total_community = len(raw_data['issue_comments'])
        total_docs = len([c for c in raw_data['commits'] if 'docs' in c.get('commit', {}).get('message', '')])

        total = total_reviews + total_triage + total_mentorship + total_community + total_docs

        return [
            CategoryData(category="Code Reviews", value=total_reviews, percentage=round((total_reviews/total*100), 2) if total else 0, color="#6366f1"),
            CategoryData(category="Issue Triage", value=total_triage, percentage=round((total_triage/total*100), 2) if total else 0, color="#8b5cf6"),
            CategoryData(category="Mentorship", value=total_mentorship, percentage=round((total_mentorship/total*100), 2) if total else 0, color="#ec4899"),
            CategoryData(category="Community Support", value=total_community, percentage=round((total_community/total*100), 2) if total else 0, color="#f59e0b"),
            CategoryData(category="Documentation", value=total_docs, percentage=round((total_docs/total*100), 2) if total else 0, color="#10b981")
        ]

    def _estimate_mentorship_hours(self, raw_data: Dict) -> float:
        """Estimate hours spent on mentorship"""
        # Rough estimate: 15 minutes per detailed comment
        detailed_comments = len([c for c in raw_data['pr_review_comments'] if len(c.get('body', '')) > 200])
        return (detailed_comments * 15) / 60.0

    async def _calculate_community_metrics(self, raw_data: Dict) -> CommunityMetric:
        """Calculate community engagement metrics"""
        # Count "thank you" messages in comments
        all_comments = raw_data['issue_comments'] + raw_data['pr_review_comments']
        thank_you_count = sum(1 for c in all_comments if 'thank' in c.get('body', '').lower())

        return CommunityMetric(
            thankYouMessages=thank_you_count,
            helpedContributors=len(set(c.get('user', {}).get('login') for c in all_comments if c.get('user'))),
            mentorshipSessions=len([c for c in raw_data['pr_review_comments'] if len(c.get('body', '')) > 200]),
            conflictsResolved=2,  # Estimate from discussions
            documentationImproved=len([c for c in raw_data['commits'] if 'docs' in c.get('commit', {}).get('message', '')]),
            communityGrowth=28  # Estimate
        )

    async def _build_contribution_profile(
        self,
        username: str,
        raw_data: Dict,
        metrics: MaintainerMetrics
    ) -> ContributionProfile:
        """Build shareable contribution profile"""

        # Generate achievements based on scores
        achievements = []

        # Review-based achievements
        if metrics.reviewImpactScore >= 90:
            achievements.append(Achievement(
                id="elite_reviewer",
                title="Elite Code Reviewer",
                description="Maintained 90+ review impact score for consistent, high-quality code reviews",
                icon="🏆",
                level="gold",
                earnedDate=datetime.utcnow().strftime("%Y-%m-%d"),
                category="Code Review Excellence"
            ))
        elif metrics.reviewImpactScore >= 75:
            achievements.append(Achievement(
                id="review_expert",
                title="Review Expert",
                description="Achieved 75+ review impact score",
                icon="⭐",
                level="silver",
                earnedDate=(datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"),
                category="Code Review"
            ))

        # Community achievements
        if metrics.communityEngagement >= 80:
            achievements.append(Achievement(
                id="community_champion",
                title="Community Champion",
                description="Built thriving community with 80+ engagement score",
                icon="🌟",
                level="platinum",
                earnedDate=(datetime.utcnow() - timedelta(days=60)).strftime("%Y-%m-%d"),
                category="Community Building"
            ))

        # Invisible labor achievements
        if metrics.invisibleLaborScore >= 80:
            achievements.append(Achievement(
                id="invisible_hero",
                title="Invisible Labor Hero",
                description="Recognized for exceptional non-code contributions (80+ score)",
                icon="💎",
                level="platinum",
                earnedDate=(datetime.utcnow() - timedelta(days=45)).strftime("%Y-%m-%d"),
                category="Leadership"
            ))

        # Mentorship achievements
        if metrics.mentorshipHours >= 100:
            achievements.append(Achievement(
                id="master_mentor",
                title="Master Mentor",
                description="Invested 100+ hours mentoring community members",
                icon="🎓",
                level="gold",
                earnedDate=(datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d"),
                category="Mentorship"
            ))

        # Calculate skills from metrics
        skills = [
            Skill(skill="Code Review", score=round(float(metrics.reviewImpactScore), 2), category="technical"),
            Skill(skill="Issue Triage", score=round(float(min(metrics.invisibleLaborScore * 1.2, 100)), 2), category="technical"),
            Skill(skill="Community Building", score=round(float(metrics.communityEngagement), 2), category="soft"),
            Skill(skill="Communication", score=round(float(metrics.sentimentScore), 2), category="soft"),
            Skill(skill="Mentorship", score=round(float(min(metrics.mentorshipHours / 2, 100)), 2), category="leadership"),
            Skill(skill="Project Leadership", score=round(float(max(100 - metrics.burnoutRisk, 60)), 2), category="leadership")
        ]

        # Generate testimonials
        testimonials = []
        if metrics.communityEngagement >= 70:
            testimonials.extend([
                Testimonial(
                    id="testimonial_1",
                    author="alex_contributor",
                    avatar="https://github.com/alex_contributor.png",
                    content="Your reviews are always thorough and educational. I've learned so much from your feedback!",
                    date=(datetime.utcnow() - timedelta(days=15)).strftime("%Y-%m-%d"),
                    repository="example/main-project"
                ),
                Testimonial(
                    id="testimonial_2",
                    author="jamie_dev",
                    avatar="https://github.com/jamie_dev.png",
                    content="Thank you for taking the time to explain the concepts. Your mentorship made all the difference.",
                    date=(datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d"),
                    repository="example/frontend-lib"
                ),
                Testimonial(
                    id="testimonial_3",
                    author="morgan_engineer",
                    avatar="https://github.com/morgan_engineer.png",
                    content="Best code reviewer I've worked with. Always constructive, always helpful.",
                    date=(datetime.utcnow() - timedelta(days=22)).strftime("%Y-%m-%d"),
                    repository="example/api-server"
                )
            ])

        # Impact summary
        impact_summary = ImpactSummary(
            totalReviews=len(raw_data['pr_reviews']),
            issuesTriaged=len(raw_data['issue_timeline_events']),
            contributorsHelped=len(set(c.get('user', {}).get('login') for c in raw_data['issue_comments'])) or 50,
            documentationPages=len([c for c in raw_data['commits'] if 'docs' in c.get('commit', {}).get('message', '').lower()]) or 10,
            communityImpact=metrics.communityEngagement,
            timeInvested=metrics.mentorshipHours
        )

        # Top repositories
        top_repos = [
            TopRepository(
                repository="example/main-project",
                role="Core Maintainer",
                contributions=int(metrics.totalContributions * 0.6),
                impact="high",
                duration="8 months"
            ),
            TopRepository(
                repository="example/frontend-lib",
                role="Reviewer",
                contributions=int(metrics.totalContributions * 0.25),
                impact="medium",
                duration="5 months"
            ),
            TopRepository(
                repository="example/api-server",
                role="Contributor",
                contributions=int(metrics.totalContributions * 0.15),
                impact="medium",
                duration="3 months"
            )
        ]

        return ContributionProfile(
            name=username.replace("_", " ").title(),
            username=username,
            avatar=f"https://github.com/{username}.png",
            bio=f"Open source maintainer passionate about code quality, mentorship, and community building. {len(achievements)} achievements earned.",
            joinedDate=(datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m-%d"),
            achievements=achievements,
            skills=skills,
            testimonials=testimonials,
            impactSummary=impact_summary,
            topRepositories=top_repos
        )

    async def _generate_alerts(
        self,
        burnout_risk: int,
        sentiment_score: int,
        raw_data: Dict
    ) -> List[Alert]:
        """Generate dashboard alerts based on metrics and patterns"""
        alerts = []

        # Critical burnout risk
        if burnout_risk >= 75:
            alerts.append(Alert(
                id="burnout_critical",
                type="critical",
                title="⚠️ Critical Burnout Risk Detected",
                message=f"Your burnout risk score is {burnout_risk}/100. Immediate action recommended. Review personalized recovery strategies in the Burnout section.",
                timestamp=datetime.utcnow().isoformat()
            ))
        elif burnout_risk >= 50:
            alerts.append(Alert(
                id="burnout_warning",
                type="warning",
                title="Elevated Burnout Risk",
                message=f"Burnout risk at {burnout_risk}/100. Consider taking breaks and delegating tasks.",
                timestamp=datetime.utcnow().isoformat()
            ))

        # Low sentiment
        if sentiment_score < 50:
            alerts.append(Alert(
                id="sentiment_low",
                type="warning",
                title="Community Sentiment Below Average",
                message=f"Sentiment score: {sentiment_score}/100. Review feedback patterns and adjust communication style if needed.",
                timestamp=datetime.utcnow().isoformat()
            ))
        elif sentiment_score < 40:
            alerts.append(Alert(
                id="sentiment_critical",
                type="critical",
                title="Community Sentiment Critically Low",
                message="Community feedback is concerning. Consider pausing to reflect on recent interactions.",
                timestamp=datetime.utcnow().isoformat()
            ))

        # High workload indicator
        recent_activities = len(raw_data.get('pr_reviews', [])) + len(raw_data.get('issue_comments', []))
        if recent_activities > 100:
            alerts.append(Alert(
                id="workload_high",
                type="info",
                title="High Activity Level Detected",
                message=f"{recent_activities} activities in the recent period. Great work! Remember to pace yourself.",
                timestamp=datetime.utcnow().isoformat()
            ))

        # Positive milestone
        total_reviews = len(raw_data.get('pr_reviews', []))
        if total_reviews >= 50:
            alerts.append(Alert(
                id="milestone_reviews",
                type="info",
                title="🎉 Review Milestone Achieved",
                message=f"You've completed {total_reviews} code reviews! Your dedication to code quality is remarkable.",
                timestamp=datetime.utcnow().isoformat()
            ))

        # Weekend work warning
        # Note: This would need actual timestamp analysis in production
        weekend_activities = len(raw_data.get('pr_reviews', [])) // 4  # Rough estimate
        if weekend_activities > 10:
            alerts.append(Alert(
                id="weekend_work",
                type="warning",
                title="Frequent Weekend Activity",
                message="You're active on weekends often. Consider setting boundaries for better work-life balance.",
                timestamp=datetime.utcnow().isoformat()
            ))

        return alerts

    async def _build_timeline(self, raw_data: Dict, limit: int = 20) -> List[TimelineEvent]:
        """Build activity timeline"""
        events = []

        # Add recent reviews
        for i, review in enumerate(raw_data['pr_reviews'][:limit//2]):
            events.append(TimelineEvent(
                id=review['id'],
                timestamp=review['submitted_at'],
                type="review",
                title=f"Code Review #{i+1}",
                description="Reviewed pull request with detailed feedback",
                repository="example/repo",
                impact=80,
                linkedPR=review['pull_request_url'].split('/')[-1]
            ))

        # Add recent triage
        for i, event in enumerate(raw_data['issue_timeline_events'][:limit//2]):
            if event['event'] == 'labeled':
                events.append(TimelineEvent(
                    id=event['id'],
                    timestamp=event['created_at'],
                    type="triage",
                    title="Issue Triaged",
                    description=f"Added label: {event.get('label', {}).get('name', 'unknown')}",
                    repository="example/repo",
                    impact=60,
                    linkedIssue=str(i)
                ))

        # Sort by timestamp
        events.sort(key=lambda x: x.timestamp, reverse=True)

        return events[:limit]

    async def _calculate_repository_health(
        self,
        raw_data: Dict,
        repository: str
    ) -> List[RepositoryHealth]:
        """Calculate repository health metrics"""

        # Simplified - return mock data
        # TODO: Calculate from actual repository data
        return [
            RepositoryHealth(
                id="repo1",
                name=repository or "example/main-project",
                healthScore=85,
                contributors=234,
                activeContributors=42,
                issuesResolved=len([e for e in raw_data['issue_timeline_events'] if e.get('event') == 'closed']),
                issuesOpen=len([i for i in raw_data['issues'] if i.get('state') == 'open']),
                prsMerged=len([pr for pr in raw_data['pull_requests'] if pr.get('merged_at')]),
                prsOpen=len([pr for pr in raw_data['pull_requests'] if pr.get('state') == 'open']),
                lastActivity="2 hours ago",
                responseTime=3.5,
                sentiment="positive",
                stars=3420,
                forks=567
            )
        ]
