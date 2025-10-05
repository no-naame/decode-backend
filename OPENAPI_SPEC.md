# OpenAPI Specification for Maintainer Dashboard Backend

## Overview

Complete OpenAPI specification with schemas/models for FastAPI backend implementation. All response types are in JSON format.

## Base Configuration

```yaml
openapi: 3.1.0
info:
  title: Maintainer Dashboard API
  version: 1.0.0
  description: API for tracking invisible labor, sentiment analysis, and OSS maintainer metrics
servers:
  - url: http://localhost:8000/api
    description: Development server
  - url: https://api.maintainer-dashboard.com
    description: Production server
```

## Authentication

```yaml
security:
  - BearerAuth: []
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

## Core Schemas/Models

### 1. User & Authentication

#### User Model

```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "name": "string",
  "avatar": "string (url)",
  "bio": "string",
  "joinedDate": "string (ISO 8601)",
  "githubId": "string",
  "role": "maintainer | contributor | admin",
  "createdAt": "string (ISO 8601)",
  "updatedAt": "string (ISO 8601)"
}
```

#### Session Model

```json
{
  "id": "string",
  "userId": "string",
  "token": "string (JWT)",
  "expiresAt": "string (ISO 8601)",
  "createdAt": "string (ISO 8601)"
}
```

### 2. Maintainer Metrics

#### MaintainerMetrics Model

```json
{
  "invisibleLaborScore": 847,
  "reviewImpactScore": 92,
  "communityEngagement": 78,
  "burnoutRisk": 42,
  "sentimentScore": 73,
  "totalRepositories": 8,
  "responseTime": 4.2,
  "totalContributions": 1247,
  "mentorshipHours": 156,
  "weeklyActivity": [
    {
      "date": "2024-03-20",
      "reviews": 15,
      "triage": 20,
      "mentorship": 10,
      "documentation": 8,
      "discussions": 12,
      "total": 65
    }
  ],
  "sentimentTrend": [
    {
      "date": "2024-03-20",
      "value": 73,
      "label": "Positive"
    }
  ],
  "activityDistribution": [
    {
      "category": "Code Reviews",
      "value": 35,
      "percentage": 35,
      "color": "#6366f1"
    }
  ]
}
```

#### ActivityData Model

```json
{
  "date": "string (YYYY-MM-DD)",
  "reviews": "integer",
  "triage": "integer",
  "mentorship": "integer",
  "documentation": "integer",
  "discussions": "integer",
  "total": "integer"
}
```

#### TrendData Model

```json
{
  "date": "string (YYYY-MM-DD)",
  "value": "number",
  "label": "string (optional)"
}
```

#### CategoryData Model

```json
{
  "category": "string",
  "value": "number",
  "percentage": "number",
  "color": "string (hex)"
}
```

### 3. Repository Health

#### RepositoryHealth Model

```json
{
  "id": "string",
  "name": "string",
  "healthScore": 85,
  "contributors": 234,
  "activeContributors": 42,
  "issuesResolved": 156,
  "issuesOpen": 23,
  "prsMerged": 89,
  "prsOpen": 12,
  "lastActivity": "2 hours ago",
  "responseTime": 3.5,
  "sentiment": "positive | neutral | negative",
  "stars": 3420,
  "forks": 567
}
```

### 4. Community Metrics

#### CommunityMetric Model

```json
{
  "thankYouMessages": 234,
  "helpedContributors": 156,
  "mentorshipSessions": 42,
  "conflictsResolved": 8,
  "documentationImproved": 23,
  "communityGrowth": 28
}
```

### 5. Burnout Indicators

#### BurnoutIndicator Model

```json
{
  "riskScore": 42,
  "riskLevel": "low | medium | high | critical",
  "indicators": {
    "workload": 65,
    "responseTime": 45,
    "sentimentDrop": 30,
    "activitySpikes": 55,
    "weekendWork": 40
  },
  "recommendations": [
    "Consider delegating code review responsibilities for 1-2 repositories",
    "Set specific 'no-code' hours to maintain work-life balance",
    "Take a 2-day break from non-critical issues",
    "Enable auto-response for weekends",
    "Schedule regular breaks between intense review sessions"
  ],
  "recoveryMetrics": {
    "daysOff": 3,
    "delegatedTasks": 12,
    "reducedScope": 20
  }
}
```

### 6. Contribution Profile

#### ContributionProfile Model

```json
{
  "name": "string",
  "username": "string",
  "avatar": "string (url)",
  "bio": "string",
  "joinedDate": "string (YYYY-MM-DD)",
  "achievements": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "icon": "string",
      "level": "bronze | silver | gold | platinum",
      "earnedDate": "string (YYYY-MM-DD)",
      "category": "string"
    }
  ],
  "skills": [
    {
      "skill": "string",
      "score": "number",
      "maxScore": 100,
      "category": "technical | soft | leadership"
    }
  ],
  "testimonials": [
    {
      "id": "string",
      "author": "string",
      "avatar": "string (url)",
      "content": "string",
      "date": "string (YYYY-MM-DD)",
      "repository": "string"
    }
  ],
  "impactSummary": {
    "totalReviews": 1247,
    "issuesTriaged": 892,
    "contributorsHelped": 156,
    "documentationPages": 45,
    "communityImpact": 94,
    "timeInvested": 1560
  },
  "topRepositories": [
    {
      "repository": "string",
      "role": "string",
      "contributions": "integer",
      "impact": "high | medium | low",
      "duration": "string"
    }
  ]
}
```

### 7. Timeline Events

#### TimelineEvent Model

```json
{
  "id": "string",
  "timestamp": "string (ISO 8601)",
  "type": "review | triage | mentorship | documentation | discussion | release",
  "title": "string",
  "description": "string",
  "repository": "string",
  "impact": "integer (0-100)",
  "linkedPR": "string (optional)",
  "linkedIssue": "string (optional)"
}
```

### 8. Sentiment Analysis

#### SentimentAnalysis Model

```json
{
  "score": 73,
  "trend": "improving | stable | declining",
  "wordFrequency": [
    {
      "word": "helpful",
      "count": 45,
      "sentiment": "positive | negative | neutral"
    }
  ],
  "feedbackDistribution": {
    "constructive": 45,
    "appreciative": 38,
    "critical": 12,
    "neutral": 5
  },
  "topPositiveFeedback": [
    "Your reviews are always thorough and educational",
    "Thank you for taking the time to explain the concepts"
  ],
  "concernAreas": [
    "Response times during weekends",
    "Some PRs take longer to review"
  ]
}
```

## API Endpoints

### Dashboard Overview

#### GET /api/dashboard/overview

**Response:** `200 OK`

```json
{
  "metrics": {
    /* MaintainerMetrics */
  },
  "alerts": [
    {
      "id": "string",
      "type": "warning | info | critical",
      "title": "string",
      "message": "string",
      "timestamp": "ISO 8601"
    }
  ],
  "recentActivity": [
    /* TimelineEvent[] */
  ]
}
```

### Maintainer Endpoints

#### GET /api/maintainer

**Query Parameters:**

- `search`: string (optional)
- `page`: integer (default: 1)
- `limit`: integer (default: 20)
- `sortBy`: string (score | activity | sentiment)

**Response:** `200 OK`

```json
{
  "maintainers": [
    {
      "id": "string",
      "username": "string",
      "name": "string",
      "avatar": "string",
      "invisibleLaborScore": 847,
      "sentiment": "positive",
      "lastActive": "ISO 8601"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "hasMore": true
  }
}
```

#### GET /api/maintainer/{id}

**Response:** `200 OK`

```json
{
  "profile": {
    /* ContributionProfile */
  },
  "metrics": {
    /* MaintainerMetrics */
  },
  "repositories": [
    /* RepositoryHealth[] */
  ]
}
```

#### GET /api/maintainer/{id}/activity

**Query Parameters:**

- `startDate`: string (YYYY-MM-DD)
- `endDate`: string (YYYY-MM-DD)
- `type`: string (review | triage | mentorship | documentation | discussion)
- `limit`: integer

**Response:** `200 OK`

```json
{
  "activities": [
    /* TimelineEvent[] */
  ],
  "summary": {
    "totalActivities": 250,
    "timeRange": {
      "start": "2024-01-01",
      "end": "2024-03-31"
    },
    "breakdown": {
      "reviews": 100,
      "triage": 50,
      "mentorship": 40,
      "documentation": 30,
      "discussions": 30
    }
  }
}
```

#### GET /api/maintainer/{id}/sentiment

**Response:** `200 OK`

```json
{
  "analysis": {
    /* SentimentAnalysis */
  },
  "history": [
    {
      "date": "2024-03-01",
      "score": 75,
      "feedback": ["string"]
    }
  ]
}
```

#### GET /api/maintainer/{id}/cv

**Response:** `200 OK`

```json
{
  "profile": {
    /* ContributionProfile */
  },
  "shareableUrl": "https://maintainer-dashboard.com/cv/username",
  "ogMetadata": {
    "title": "string",
    "description": "string",
    "image": "string (url)"
  }
}
```

### Repository Health Endpoints

#### GET /api/repositories

**Response:** `200 OK`

```json
{
  "repositories": [
    /* RepositoryHealth[] */
  ],
  "summary": {
    "totalRepositories": 8,
    "healthyCount": 4,
    "needsAttentionCount": 3,
    "criticalCount": 1,
    "totalContributors": 234
  }
}
```

#### GET /api/repositories/{id}/health

**Response:** `200 OK`

```json
{
  "repository": {
    /* RepositoryHealth */
  },
  "trends": {
    "contributorGrowth": [
      /* TrendData[] */
    ],
    "issueResolution": [
      /* TrendData[] */
    ],
    "prVelocity": [
      /* TrendData[] */
    ]
  },
  "topContributors": [
    {
      "id": "string",
      "username": "string",
      "avatar": "string",
      "contributions": 45
    }
  ]
}
```

### Burnout Assessment Endpoints

#### GET /api/burnout/assessment

**Response:** `200 OK`

```json
{
  "indicator": {
    /* BurnoutIndicator */
  },
  "trends": {
    "workload": [
      /* TrendData[] */
    ],
    "responseTime": [
      /* TrendData[] */
    ],
    "sentiment": [
      /* TrendData[] */
    ]
  },
  "warnings": [
    {
      "sign": "string",
      "status": "ok | warning | alert",
      "description": "string"
    }
  ]
}
```

#### POST /api/burnout/recommendations

**Request Body:**

```json
{
  "maintainerId": "string",
  "indicators": {
    /* partial BurnoutIndicator */
  }
}
```

**Response:** `200 OK`

```json
{
  "recommendations": ["string"],
  "priority": "low | medium | high | critical",
  "suggestedActions": [
    {
      "action": "string",
      "impact": "high | medium | low",
      "effort": "low | medium | high"
    }
  ]
}
```

### Timeline & Activity Endpoints

#### GET /api/timeline

**Query Parameters:**

- `startDate`: string
- `endDate`: string
- `type`: string (optional)
- `repository`: string (optional)

**Response:** `200 OK`

```json
{
  "events": [
    /* TimelineEvent[] */
  ],
  "summary": {
    "totalEvents": 150,
    "impactScore": 847,
    "mostActiveRepository": "string",
    "peakActivity": {
      "date": "2024-03-25",
      "count": 25
    }
  }
}
```

#### GET /api/timeline/hourly

**Query Parameters:**

- `date`: string (YYYY-MM-DD)

**Response:** `200 OK`

```json
{
  "hourlyActivity": [
    {
      "hour": 0,
      "reviews": 2,
      "triage": 5,
      "mentorship": 1,
      "documentation": 0,
      "discussions": 3
    }
  ],
  "peak": {
    "hour": 14,
    "total": 25
  }
}
```

### Community Metrics Endpoints

#### GET /api/community/metrics

**Response:** `200 OK`

```json
{
  "metrics": {
    /* CommunityMetric */
  },
  "trends": {
    "growth": [
      /* TrendData[] */
    ],
    "engagement": [
      /* TrendData[] */
    ],
    "satisfaction": [
      /* TrendData[] */
    ]
  }
}
```

### Charts & Visualizations Data

#### GET /api/charts/activity-distribution

**Response:** `200 OK`

```json
{
  "data": [
    /* CategoryData[] */
  ],
  "total": 100,
  "period": "7d | 30d | 90d | 1y"
}
```

#### GET /api/charts/weekly-activity

**Response:** `200 OK`

```json
{
  "data": [
    /* ActivityData[] */
  ],
  "summary": {
    "totalActivities": 250,
    "averagePerDay": 35.7,
    "mostActiveDay": "Monday",
    "trend": "increasing | stable | decreasing"
  }
}
```

#### GET /api/charts/sentiment-trend

**Response:** `200 OK`

```json
{
  "data": [
    /* TrendData[] */
  ],
  "currentScore": 73,
  "trend": "improving | stable | declining",
  "averageScore": 68.5
}
```

#### GET /api/charts/heatmap

**Query Parameters:**

- `startDate`: string
- `endDate`: string

**Response:** `200 OK`

```json
{
  "data": [
    {
      "day": "Monday",
      "hour": "14:00",
      "intensity": 85
    }
  ],
  "peakTimes": [
    {
      "day": "string",
      "hour": "string",
      "intensity": "number"
    }
  ]
}
```

#### GET /api/charts/radar-skills

**Response:** `200 OK`

```json
{
  "data": [
    {
      "skill": "Code Review",
      "value": 95,
      "fullMark": 100
    }
  ],
  "categories": ["technical", "soft", "leadership"]
}
```

### Export & PDF Generation

#### POST /api/export/pdf

**Request Body:**

```json
{
  "url": "string",
  "filename": "string",
  "options": {
    "format": "A4 | Letter",
    "landscape": false,
    "margins": {
      "top": "20px",
      "bottom": "20px",
      "left": "20px",
      "right": "20px"
    }
  }
}
```

**Response:** `200 OK`

```
Content-Type: application/pdf
[Binary PDF Data]
```

### Milestone Celebrations (Future)

#### GET /api/milestones

**Response:** `200 OK`

```json
{
  "milestones": [
    {
      "id": "string",
      "type": "stars | prs | anniversary | contributors | release",
      "title": "1000 Stars Reached!",
      "description": "string",
      "achievedDate": "ISO 8601",
      "repository": "string",
      "value": 1000,
      "celebrationUrl": "string"
    }
  ]
}
```

#### POST /api/milestones/{id}/generate-post

**Request Body:**

```json
{
  "platform": "linkedin | twitter",
  "template": "string (optional)"
}
```

**Response:** `200 OK`

```json
{
  "post": {
    "text": "string",
    "hashtags": ["#opensource", "#milestone"],
    "image": "string (url)",
    "shareUrl": "string"
  }
}
```

### Project Discovery (Future)

#### GET /api/projects/search

**Query Parameters:**

- `q`: string (search query)
- `language`: string[]
- `healthScore`: integer (min)
- `stars`: integer (min)
- `activity`: string (active | moderate | low)
- `compatibility`: string[]

**Response:** `200 OK`

```json
{
  "projects": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "language": "string",
      "healthScore": 85,
      "stars": 5000,
      "forks": 500,
      "contributors": 100,
      "lastActivity": "ISO 8601",
      "tags": ["string"],
      "compatibility": ["beginner-friendly", "good-first-issues"]
    }
  ],
  "facets": {
    "languages": { "JavaScript": 45, "TypeScript": 30 },
    "healthScores": { "80-100": 20, "60-79": 35 },
    "activity": { "active": 50, "moderate": 30 }
  },
  "total": 250
}
```

#### GET /api/projects/{id}

**Response:** `200 OK`

```json
{
  "project": {
    "id": "string",
    "name": "string",
    "fullName": "owner/repo",
    "description": "string",
    "readme": "string (markdown)",
    "language": "string",
    "languages": { "JavaScript": 60, "TypeScript": 40 },
    "topics": ["string"],
    "healthScore": 85,
    "stats": {
      "stars": 5000,
      "forks": 500,
      "watchers": 200,
      "openIssues": 45,
      "openPRs": 12
    },
    "activity": {
      "lastCommit": "ISO 8601",
      "lastRelease": "ISO 8601",
      "commitsPerWeek": [15, 20, 18, 22, 25, 30, 28]
    },
    "maintainers": [
      {
        "username": "string",
        "avatar": "string",
        "role": "string"
      }
    ],
    "contributionGuide": "string (url)",
    "codeOfConduct": "string (url)"
  }
}
```

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {
      "field": "string",
      "reason": "string"
    },
    "timestamp": "ISO 8601"
  }
}
```

### Common Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Internal Server Error

## Rate Limiting

```json
{
  "X-RateLimit-Limit": "1000",
  "X-RateLimit-Remaining": "999",
  "X-RateLimit-Reset": "1625097600"
}
```

## Pagination

Standard pagination format for all list endpoints:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5,
    "hasNext": true,
    "hasPrev": false
  }
}
```

## WebSocket Events (Real-time)

### Connection

```json
{
  "event": "connect",
  "data": {
    "sessionId": "string",
    "userId": "string"
  }
}
```

### Activity Update

```json
{
  "event": "activity.update",
  "data": {
    "type": "review | triage | mentorship",
    "activity": {
      /* TimelineEvent */
    }
  }
}
```

### Sentiment Change

```json
{
  "event": "sentiment.change",
  "data": {
    "previousScore": 70,
    "currentScore": 75,
    "trend": "improving"
  }
}
```

### Burnout Alert

```json
{
  "event": "burnout.alert",
  "data": {
    "level": "warning | critical",
    "indicator": {
      /* BurnoutIndicator */
    },
    "recommendation": "string"
  }
}
```

## FastAPI Implementation Notes

### Model Definitions

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class MaintainerMetrics(BaseModel):
    invisible_labor_score: int = Field(..., ge=0, le=1000)
    review_impact_score: int = Field(..., ge=0, le=100)
    community_engagement: int = Field(..., ge=0, le=100)
    burnout_risk: int = Field(..., ge=0, le=100)
    sentiment_score: int = Field(..., ge=0, le=100)
    total_repositories: int = Field(..., ge=0)
    response_time: float = Field(..., ge=0)
    total_contributions: int = Field(..., ge=0)
    mentorship_hours: int = Field(..., ge=0)
    weekly_activity: List[ActivityData]
    sentiment_trend: List[TrendData]
    activity_distribution: List[CategoryData]
```

### Cache Strategy

- Static data: 5 minutes
- User profiles: 1 minute
- Real-time data: No cache
- Charts: 30 seconds

### Database Schema

- PostgreSQL for structured data
- Redis for caching
- TimescaleDB for time-series data
- Elasticsearch for search functionality

### Authentication Flow

1. OAuth with GitHub
2. JWT tokens with refresh
3. Session storage in Redis
4. Rate limiting per user

## Testing

### Example cURL Requests

```bash
# Get dashboard overview
curl -X GET "http://localhost:8000/api/dashboard/overview" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get maintainer profile
curl -X GET "http://localhost:8000/api/maintainer/alexchen" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Export PDF
curl -X POST "http://localhost:8000/api/export/pdf" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://localhost:3000/dashboard",
    "filename": "dashboard-export"
  }'
```

---

This specification provides a complete blueprint for implementing the FastAPI backend with all necessary models, endpoints, and response formats for the maintainer dashboard application.
