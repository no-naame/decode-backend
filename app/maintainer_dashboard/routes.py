"""
Single Dashboard Endpoint

Simplified API with one main endpoint that returns all dashboard data.
"""
from fastapi import APIRouter, HTTPException, Query
from .service import DashboardService
from .schemas import DashboardOverviewResponse

router = APIRouter()
service = DashboardService()


@router.get("/{username}", response_model=DashboardOverviewResponse)
async def get_dashboard(
    username: str,
    repository: str = Query(default=None, description="Optional repository filter (owner/repo)"),
    days: int = Query(default=30, ge=7, le=365, description="Time window in days")
):
    """
    **GET COMPLETE MAINTAINER DASHBOARD DATA**

    Single endpoint that returns ALL data needed for the frontend dashboard.

    **Returns:**
    - **Metrics**: Invisible labor score, review impact, community engagement, burnout risk, sentiment
    - **Burnout Assessment**: Risk level, indicators, AI-generated recommendations
    - **Sentiment Analysis**: Score, trend, word frequency, feedback distribution
    - **Community Metrics**: Thank you messages, helped contributors, mentorship sessions
    - **Contribution Profile**: Achievements, skills, testimonials, impact summary
    - **Alerts**: Critical warnings and notifications
    - **Recent Activity**: Timeline of recent contributions
    - **Repository Health**: Health scores, contributor stats, sentiment

    **Parameters:**
    - `username` (path): GitHub username to analyze
    - `repository` (query, optional): Filter by specific repository (format: "owner/repo")
    - `days` (query, default=30): Time window for analysis (7-365 days)

    **Example Request:**
    ```
    GET /api/dashboard/sarah_maintainer?repository=example/repo&days=30
    ```

    **Example Response:**
    ```json
    {
      "metrics": {
        "invisibleLaborScore": 85,
        "reviewImpactScore": 92,
        "communityEngagement": 78,
        "burnoutRisk": 42,
        "sentimentScore": 73,
        "totalRepositories": 3,
        "responseTime": 4.5,
        "totalContributions": 247,
        "mentorshipHours": 156.5,
        "weeklyActivity": [
          {"date": "2024-03-20", "reviews": 15, "triage": 20, "mentorship": 10, "documentation": 8, "discussions": 12, "total": 65}
        ],
        "sentimentTrend": [
          {"date": "2024-03-20", "value": 73, "label": "Positive"}
        ],
        "activityDistribution": [
          {"category": "Code Reviews", "value": 35, "percentage": 35, "color": "#6366f1"}
        ]
      },
      "burnout": {
        "riskScore": 42,
        "riskLevel": "medium",
        "indicators": {
          "workload": 65,
          "responseTime": 45,
          "sentimentDrop": 30,
          "activitySpikes": 55,
          "weekendWork": 40
        },
        "recommendations": [
          "Consider delegating code review responsibilities",
          "Set specific 'no-code' hours for work-life balance"
        ],
        "recoveryMetrics": {"daysOff": 3, "delegatedTasks": 12, "reducedScope": 20}
      },
      "sentiment": {
        "score": 73,
        "trend": "improving",
        "wordFrequency": [
          {"word": "helpful", "count": 45, "sentiment": "positive"}
        ],
        "feedbackDistribution": {"constructive": 45, "appreciative": 38, "critical": 12, "neutral": 5},
        "topPositiveFeedback": ["Your reviews are thorough and educational"],
        "concernAreas": ["Response times during weekends"]
      },
      "communityMetrics": {
        "thankYouMessages": 234,
        "helpedContributors": 156,
        "mentorshipSessions": 42,
        "conflictsResolved": 8,
        "documentationImproved": 23,
        "communityGrowth": 28
      },
      "profile": {
        "name": "Sarah Maintainer",
        "username": "sarah_maintainer",
        "achievements": [
          {"id": "elite_reviewer", "title": "Elite Code Reviewer", "level": "gold", "category": "Code Review Excellence"}
        ],
        "skills": [
          {"skill": "Code Review", "score": 92, "category": "technical"}
        ],
        "testimonials": [
          {"author": "alex_contributor", "content": "Your reviews are always thorough and educational!"}
        ]
      },
      "alerts": [
        {"id": "burnout_warning", "type": "warning", "title": "Elevated Burnout Risk", "message": "Burnout risk at 42/100"}
      ],
      "recentActivity": [
        {"id": "rv1", "type": "review", "title": "Code Review #1", "repository": "example/repo", "impact": 80}
      ],
      "repositoryHealth": [
        {"id": "repo1", "name": "example/main-project", "healthScore": 85, "contributors": 234, "sentiment": "positive"}
      ]
    }
    ```

    **Calculation Methods:**

    All metrics are calculated using rigorous, documented formulas:

    1. **Invisible Labor Score (0-100)**:
       - Code Reviews (35%): 1 pt/review + depth multiplier
       - Issue Triage (25%): 0.5-1.5 pts per action
       - Mentorship (20%): 1.2 pts per detailed comment
       - Community (15%): 0.3-1 pts per interaction
       - Documentation (5%): 1.5-2 pts per commit

    2. **Review Impact (0-100)**:
       - Thoroughness (40%): Comments, lines reviewed
       - Timeliness (30%): Response time
       - Helpfulness (30%): Approval ratio

    3. **Community Engagement (0-100)**:
       - Participation (50%): Total activity
       - Helpfulness (30%): Reactions, answers
       - Responsiveness (20%): Quick replies

    4. **Burnout Risk (0-100)**:
       - Workload (30%): Activities per day
       - Irregular Hours (25%): Weekend/late night work
       - Sentiment Decline (25%): Mood tracking
       - Response Pressure (20%): Activity density

    5. **Sentiment Score (0-100)**:
       - Positive feedback percentage
       - Tone analysis of interactions
       - Word frequency analysis

    **AI Features:**
    - Persona identification
    - Burnout recovery recommendations
    - Sentiment feedback analysis
    - Impact summaries

    All AI outputs are grounded in actual numeric data to prevent hallucination.

    **Data Sources:**
    - GitHub REST API (PRs, issues, comments, reviews)
    - GitHub GraphQL API (discussions)
    - Database (cached metrics, historical data)

    **Error Responses:**
    - `404`: User not found
    - `500`: Server error (check logs for details)
    """
    try:
        dashboard_data = await service.get_complete_dashboard(
            username=username,
            repository=repository,
            days=days
        )
        return dashboard_data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Maintainer Dashboard",
        "version": "2.0.0",
        "endpoints": {
            "main": "GET /api/dashboard/{username}",
            "health": "GET /api/dashboard/health"
        },
        "features": [
            "Single unified endpoint",
            "Rigorous metric calculations",
            "AI insights with anti-hallucination",
            "Complete dashboard data"
        ]
    }
