# Complete OpenAPI Specification - All Fields Required by Frontend

## Overview

This specification includes EVERY field needed by the frontend, including those currently being generated locally. The backend should populate ALL these fields.

## Endpoint

### GET /api/v1/dashboard/{username}

**Path Parameters:**

- `username`: string (GitHub username)

**Response:** `200 OK`

```json
{
  "metrics": {
    "invisibleLaborScore": 21,
    "reviewImpactScore": 52,
    "communityEngagement": 95,
    "burnoutRisk": 62,
    "sentimentScore": 73,
    "totalRepositories": 1,
    "responseTime": 4.5,
    "totalContributions": 103,
    "mentorshipHours": 0,
    "weeklyActivity": [
      {
        "date": "2025-09-07",
        "reviews": 5,
        "triage": 8,
        "mentorship": 3,
        "documentation": 2,
        "discussions": 4,
        "total": 22
      }
    ],
    "sentimentTrend": [
      {
        "date": "2025-09-07",
        "value": 70,
        "label": "Positive"
      }
    ],
    "activityDistribution": [
      {
        "category": "Code Reviews",
        "value": 18,
        "percentage": 17.647058823529413,
        "color": "#6366f1"
      },
      {
        "category": "Issue Triage",
        "value": 50,
        "percentage": 49.01960784313725,
        "color": "#8b5cf6"
      },
      {
        "category": "Mentorship",
        "value": 0,
        "percentage": 0,
        "color": "#ec4899"
      },
      {
        "category": "Community Support",
        "value": 30,
        "percentage": 29.411764705882355,
        "color": "#f59e0b"
      },
      {
        "category": "Documentation",
        "value": 4,
        "percentage": 3.9215686274509802,
        "color": "#10b981"
      }
    ]
  },
  "burnout": {
    "riskScore": 62,
    "riskLevel": "high",
    "indicators": {
      "workload": 34,
      "responseTime": 100,
      "sentimentDrop": 27,
      "activitySpikes": 34,
      "weekendWork": 65
    },
    "recommendations": [
      "Reduce daily code reviews from current load by 30%",
      "Set specific no-code hours (6PM-9AM) in settings"
    ],
    "recoveryMetrics": {
      "daysOff": 0,
      "delegatedTasks": 0,
      "reducedScope": 0
    },
    "trends": {
      "responseTime": [
        {
          "date": "2025-09-01",
          "value": 4.2
        },
        {
          "date": "2025-09-02",
          "value": 4.5
        }
      ],
      "activityLevel": [
        {
          "date": "2025-09-01",
          "value": 65
        },
        {
          "date": "2025-09-02",
          "value": 68
        }
      ],
      "sentiment": [
        {
          "date": "2025-09-01",
          "value": 73
        },
        {
          "date": "2025-09-02",
          "value": 75
        }
      ]
    }
  },
  "sentiment": {
    "score": 73,
    "trend": "stable",
    "wordFrequency": [
      {
        "word": "helpful",
        "count": 45,
        "sentiment": "positive"
      }
    ],
    "feedbackDistribution": {
      "constructive": 45,
      "appreciative": 38,
      "critical": 12,
      "neutral": 5
    },
    "topPositiveFeedback": ["Reviews provide clear, actionable feedback"],
    "concernAreas": [
      "Review tone generally good with room for more positive reinforcement"
    ],
    "multiLineTrend": {
      "overall": [
        {
          "date": "2025-08-01",
          "value": 70
        },
        {
          "date": "2025-08-02",
          "value": 71
        }
      ],
      "reviews": [
        {
          "date": "2025-08-01",
          "value": 72
        },
        {
          "date": "2025-08-02",
          "value": 73
        }
      ],
      "discussions": [
        {
          "date": "2025-08-01",
          "value": 68
        },
        {
          "date": "2025-08-02",
          "value": 69
        }
      ]
    }
  },
  "communityMetrics": {
    "thankYouMessages": 30,
    "helpedContributors": 0,
    "mentorshipSessions": 0,
    "conflictsResolved": 2,
    "documentationImproved": 4,
    "communityGrowth": 28
  },
  "profile": {
    "name": "Sarah Maintainer",
    "username": "sarah_maintainer",
    "avatar": "https://github.com/sarah_maintainer.png",
    "bio": "Open source maintainer focused on code quality and community growth",
    "joinedDate": "2024-10-05",
    "achievements": [],
    "skills": [
      {
        "skill": "Code Review",
        "score": 52,
        "maxScore": 100,
        "category": "technical"
      }
    ],
    "testimonials": [],
    "impactSummary": {
      "totalReviews": 18,
      "issuesTriaged": 50,
      "contributorsHelped": 50,
      "documentationPages": 10,
      "communityImpact": 95,
      "timeInvested": 0
    },
    "topRepositories": [
      {
        "repository": "example/main-project",
        "role": "Core Maintainer",
        "contributions": 103,
        "impact": "high",
        "duration": "6 months"
      }
    ],
    "skillsRadar": [
      {
        "skill": "Code Review",
        "value": 95,
        "fullMark": 100
      },
      {
        "skill": "Issue Triage",
        "value": 88,
        "fullMark": 100
      },
      {
        "skill": "Mentorship",
        "value": 92,
        "fullMark": 100
      },
      {
        "skill": "Documentation",
        "value": 78,
        "fullMark": 100
      },
      {
        "skill": "Conflict Resolution",
        "value": 85,
        "fullMark": 100
      },
      {
        "skill": "Community Building",
        "value": 90,
        "fullMark": 100
      }
    ]
  },
  "alerts": [],
  "recentActivity": [
    {
      "id": "e0",
      "timestamp": "2025-10-05T00:12:19.539969Z",
      "type": "triage",
      "title": "Issue Triaged",
      "description": "Added label: bug",
      "repository": "example/repo",
      "impact": 60,
      "linkedPR": null,
      "linkedIssue": "0"
    }
  ],
  "repositoryHealth": [
    {
      "id": "repo1",
      "name": "example/main-project",
      "healthScore": 85,
      "contributors": 234,
      "activeContributors": 42,
      "issuesResolved": 16,
      "issuesOpen": 20,
      "prsMerged": 0,
      "prsOpen": 0,
      "lastActivity": "2 hours ago",
      "responseTime": 3.5,
      "sentiment": "positive",
      "stars": 3420,
      "forks": 567
    }
  ],
  "analytics": {
    "activityHeatmap": [
      {
        "day": "Monday",
        "hour": 0,
        "intensity": 45
      },
      {
        "day": "Monday",
        "hour": 1,
        "intensity": 12
      },
      {
        "day": "Monday",
        "hour": 14,
        "intensity": 85
      }
    ],
    "contributorGrowth": {
      "total": [
        {
          "date": "2025-09-01",
          "value": 150
        },
        {
          "date": "2025-09-02",
          "value": 152
        }
      ],
      "new": [
        {
          "date": "2025-09-01",
          "value": 5
        },
        {
          "date": "2025-09-02",
          "value": 6
        }
      ],
      "returning": [
        {
          "date": "2025-09-01",
          "value": 120
        },
        {
          "date": "2025-09-02",
          "value": 122
        }
      ]
    },
    "issueResolutionFunnel": [
      {
        "stage": "Created",
        "count": 234,
        "percentage": 100
      },
      {
        "stage": "Triaged",
        "count": 198,
        "percentage": 85
      },
      {
        "stage": "Assigned",
        "count": 156,
        "percentage": 67
      },
      {
        "stage": "In Progress",
        "count": 112,
        "percentage": 48
      },
      {
        "stage": "Resolved",
        "count": 98,
        "percentage": 42
      }
    ],
    "impactTimeline": [
      {
        "date": "2025-03-25",
        "type": "review",
        "title": "Security Fix Review",
        "impact": 95,
        "responses": 12,
        "color": "blue-500"
      },
      {
        "date": "2025-03-20",
        "type": "mentorship",
        "title": "Onboarded 5 New Contributors",
        "impact": 85,
        "responses": 8,
        "color": "purple-500"
      },
      {
        "date": "2025-03-15",
        "type": "triage",
        "title": "Organized 50+ Issues for v2.0",
        "impact": 78,
        "responses": 5,
        "color": "emerald-500"
      },
      {
        "date": "2025-03-10",
        "type": "documentation",
        "title": "Rewrote API Documentation",
        "impact": 72,
        "responses": 15,
        "color": "amber-500"
      }
    ],
    "cumulativeLabor": [
      {
        "date": "2025-09-01",
        "reviews": 5,
        "triage": 8,
        "mentorship": 3,
        "documentation": 2,
        "discussions": 4
      },
      {
        "date": "2025-09-02",
        "reviews": 12,
        "triage": 16,
        "mentorship": 7,
        "documentation": 4,
        "discussions": 9
      }
    ]
  }
}
```

## NEW FIELDS TO ADD (Currently Generated in Frontend)

### 1. `burnout.trends` Object

**Location:** `app/dashboard/burnout/page.tsx` - `generateBurnoutTrends()`

```typescript
"trends": {
  "responseTime": [{"date": "YYYY-MM-DD", "value": number}],  // 30 days
  "activityLevel": [{"date": "YYYY-MM-DD", "value": number}], // 30 days
  "sentiment": [{"date": "YYYY-MM-DD", "value": number}]      // 30 days
}
```

### 2. `sentiment.multiLineTrend` Object

**Location:** `app/dashboard/sentiment/page.tsx` - `generateMultiLineSentiment()`

```typescript
"multiLineTrend": {
  "overall": [{"date": "YYYY-MM-DD", "value": number}],     // 90 days
  "reviews": [{"date": "YYYY-MM-DD", "value": number}],     // 90 days
  "discussions": [{"date": "YYYY-MM-DD", "value": number}]  // 90 days
}
```

### 3. `profile.skillsRadar` Array

**Location:** `app/dashboard/invisible-labor/page.tsx` - `radarData`

```typescript
"skillsRadar": [
  {
    "skill": "Code Review",
    "value": 95,      // 0-100
    "fullMark": 100
  },
  {
    "skill": "Issue Triage",
    "value": 88,
    "fullMark": 100
  },
  {
    "skill": "Mentorship",
    "value": 92,
    "fullMark": 100
  },
  {
    "skill": "Documentation",
    "value": 78,
    "fullMark": 100
  },
  {
    "skill": "Conflict Resolution",
    "value": 85,
    "fullMark": 100
  },
  {
    "skill": "Community Building",
    "value": 90,
    "fullMark": 100
  }
]
```

### 4. `analytics` Object (NEW TOP-LEVEL FIELD)

#### 4.1 `analytics.activityHeatmap` Array

**Location:** `app/dashboard/invisible-labor/page.tsx` - `heatMapData`

```typescript
"activityHeatmap": [
  {
    "day": "Monday",  // or "Tuesday", "Wednesday", etc.
    "hour": 0,        // 0-23
    "intensity": 45   // 0-100
  }
  // 168 entries total (7 days × 24 hours)
]
```

#### 4.2 `analytics.contributorGrowth` Object

**Location:** `app/dashboard/repositories/page.tsx` - `generateContributorGrowth()`

```typescript
"contributorGrowth": {
  "total": [
    {"date": "YYYY-MM-DD", "value": 150}  // 30 days
  ],
  "new": [
    {"date": "YYYY-MM-DD", "value": 5}    // 30 days
  ],
  "returning": [
    {"date": "YYYY-MM-DD", "value": 120}  // 30 days
  ]
}
```

#### 4.3 `analytics.issueResolutionFunnel` Array

**Location:** `app/dashboard/repositories/page.tsx` - `issueResolutionData`

```typescript
"issueResolutionFunnel": [
  {
    "stage": "Created",
    "count": 234,
    "percentage": 100
  },
  {
    "stage": "Triaged",
    "count": 198,
    "percentage": 85
  },
  {
    "stage": "Assigned",
    "count": 156,
    "percentage": 67
  },
  {
    "stage": "In Progress",
    "count": 112,
    "percentage": 48
  },
  {
    "stage": "Resolved",
    "count": 98,
    "percentage": 42
  }
]
```

#### 4.4 `analytics.impactTimeline` Array

**Location:** `app/dashboard/invisible-labor/page.tsx` - hardcoded events

```typescript
"impactTimeline": [
  {
    "date": "2025-03-25",
    "type": "review",        // or "mentorship", "triage", "documentation"
    "title": "Security Fix Review",
    "impact": 95,            // 0-100
    "responses": 12,
    "color": "blue-500"      // Tailwind color class
  }
]
```

#### 4.5 `analytics.cumulativeLabor` Array

**Location:** `app/dashboard/invisible-labor/page.tsx` - uses `metrics.weeklyActivity` but needs cumulative

```typescript
"cumulativeLabor": [
  {
    "date": "YYYY-MM-DD",
    "reviews": 5,
    "triage": 8,
    "mentorship": 3,
    "documentation": 2,
    "discussions": 4
  }
  // 30 days of cumulative data
]
```

## Complete TypeScript Interface

```typescript
interface DashboardResponse {
  metrics: {
    invisibleLaborScore: number;
    reviewImpactScore: number;
    communityEngagement: number;
    burnoutRisk: number;
    sentimentScore: number;
    totalRepositories: number;
    responseTime: number;
    totalContributions: number;
    mentorshipHours: number;
    weeklyActivity: Array<{
      date: string;
      reviews: number;
      triage: number;
      mentorship: number;
      documentation: number;
      discussions: number;
      total: number;
    }>;
    sentimentTrend: Array<{
      date: string;
      value: number;
      label: string;
    }>;
    activityDistribution: Array<{
      category: string;
      value: number;
      percentage: number;
      color: string;
    }>;
  };
  burnout: {
    riskScore: number;
    riskLevel: "low" | "medium" | "high" | "critical";
    indicators: {
      workload: number;
      responseTime: number;
      sentimentDrop: number;
      activitySpikes: number;
      weekendWork: number;
    };
    recommendations: string[];
    recoveryMetrics: {
      daysOff: number;
      delegatedTasks: number;
      reducedScope: number;
    };
    trends: {
      responseTime: Array<{ date: string; value: number }>;
      activityLevel: Array<{ date: string; value: number }>;
      sentiment: Array<{ date: string; value: number }>;
    };
  };
  sentiment: {
    score: number;
    trend: "improving" | "stable" | "declining";
    wordFrequency: Array<{
      word: string;
      count: number;
      sentiment: "positive" | "negative" | "neutral";
    }>;
    feedbackDistribution: {
      constructive: number;
      appreciative: number;
      critical: number;
      neutral: number;
    };
    topPositiveFeedback: string[];
    concernAreas: string[];
    multiLineTrend: {
      overall: Array<{ date: string; value: number }>;
      reviews: Array<{ date: string; value: number }>;
      discussions: Array<{ date: string; value: number }>;
    };
  };
  communityMetrics: {
    thankYouMessages: number;
    helpedContributors: number;
    mentorshipSessions: number;
    conflictsResolved: number;
    documentationImproved: number;
    communityGrowth: number;
  };
  profile: {
    name: string;
    username: string;
    avatar: string;
    bio: string;
    joinedDate: string;
    achievements: Array<{
      id: string;
      title: string;
      description: string;
      icon: string;
      level: "bronze" | "silver" | "gold" | "platinum";
      earnedDate: string;
      category: string;
    }>;
    skills: Array<{
      skill: string;
      score: number;
      maxScore: number;
      category: "technical" | "soft" | "leadership";
    }>;
    testimonials: Array<{
      id: string;
      author: string;
      avatar: string;
      content: string;
      date: string;
      repository: string;
    }>;
    impactSummary: {
      totalReviews: number;
      issuesTriaged: number;
      contributorsHelped: number;
      documentationPages: number;
      communityImpact: number;
      timeInvested: number;
    };
    topRepositories: Array<{
      repository: string;
      role: string;
      contributions: number;
      impact: "high" | "medium" | "low";
      duration: string;
    }>;
    skillsRadar: Array<{
      skill: string;
      value: number;
      fullMark: number;
    }>;
  };
  alerts: Array<{
    id: string;
    type: "info" | "warning" | "critical";
    title: string;
    message: string;
    timestamp: string;
  }>;
  recentActivity: Array<{
    id: string;
    timestamp: string;
    type:
      | "review"
      | "triage"
      | "mentorship"
      | "documentation"
      | "discussion"
      | "release";
    title: string;
    description: string;
    repository: string;
    impact: number;
    linkedPR: string | null;
    linkedIssue: string | null;
  }>;
  repositoryHealth: Array<{
    id: string;
    name: string;
    healthScore: number;
    contributors: number;
    activeContributors: number;
    issuesResolved: number;
    issuesOpen: number;
    prsMerged: number;
    prsOpen: number;
    lastActivity: string;
    responseTime: number;
    sentiment: "positive" | "neutral" | "negative";
    stars: number;
    forks: number;
  }>;
  analytics: {
    activityHeatmap: Array<{
      day: string;
      hour: number;
      intensity: number;
    }>;
    contributorGrowth: {
      total: Array<{ date: string; value: number }>;
      new: Array<{ date: string; value: number }>;
      returning: Array<{ date: string; value: number }>;
    };
    issueResolutionFunnel: Array<{
      stage: string;
      count: number;
      percentage: number;
    }>;
    impactTimeline: Array<{
      date: string;
      type: string;
      title: string;
      impact: number;
      responses: number;
      color: string;
    }>;
    cumulativeLabor: Array<{
      date: string;
      reviews: number;
      triage: number;
      mentorship: number;
      documentation: number;
      discussions: number;
    }>;
  };
}
```

## Summary of Missing Fields

### Currently in API ✓

- metrics (all fields)
- burnout (core fields)
- sentiment (core fields)
- communityMetrics
- profile (core fields)
- alerts
- recentActivity
- repositoryHealth

### NEED TO ADD ❌

1. **burnout.trends** - 30-day trend data for 3 metrics
2. **sentiment.multiLineTrend** - 90-day sentiment evolution
3. **profile.skillsRadar** - 6 skill assessments for radar chart
4. **analytics** - NEW top-level object with:
   - **activityHeatmap** - 7 days × 24 hours = 168 data points
   - **contributorGrowth** - 30-day trends for 3 metrics
   - **issueResolutionFunnel** - 5-stage funnel data
   - **impactTimeline** - Major contribution events
   - **cumulativeLabor** - 30-day cumulative activity

## Data Generation Guidelines

### Time Ranges

- **weeklyActivity**: Last 7 days (or 4 weeks as shown in your response)
- **sentimentTrend**: Last 30 days
- **burnout.trends**: Last 30 days
- **sentiment.multiLineTrend**: Last 90 days
- **activityHeatmap**: Last 7 days
- **contributorGrowth**: Last 30 days
- **cumulativeLabor**: Last 30 days

### Date Format

- Use `YYYY-MM-DD` format for all dates
- Use ISO 8601 for timestamps: `YYYY-MM-DDTHH:mm:ss.SSSZ`

### Skill Categories

Use these exact skill names for `skillsRadar`:

1. "Code Review"
2. "Issue Triage"
3. "Mentorship"
4. "Documentation"
5. "Conflict Resolution"
6. "Community Building"

### Activity Types

- "review"
- "triage"
- "mentorship"
- "documentation"
- "discussion"
- "release"

### Days of Week

- "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"