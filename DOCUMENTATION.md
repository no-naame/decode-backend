# Maintainer Dashboard Dummy Data Documentation

## Overview
This document explains the comprehensive dummy data structure designed to test your maintainer dashboard. The data mimics real GitHub API and Ecosyste.ms responses and includes all necessary information for:

1. **Invisible Labor Scoring System**
2. **Sentiment Analysis Engine**
3. **Burnout Risk Detection**
4. **Shareable Contribution Profile**

## Table of Contents
1. [Data Structure Overview](#data-structure-overview)
2. [GitHub API Mapping](#github-api-mapping)
3. [Maintainer Personas](#maintainer-personas)
4. [Data Patterns & Scenarios](#data-patterns--scenarios)
5. [Testing Your Dashboard](#testing-your-dashboard)
6. [Sample Queries](#sample-queries)

---

## Data Structure Overview

### Core Tables

#### 1. **maintainers**
Represents GitHub users who are contributors/maintainers.

**Maps to GitHub API**: `/users/{username}`

**Key Fields**:
- `github_id`: Unique GitHub user ID
- `username`: GitHub username
- `name`, `email`, `bio`, `company`, `location`: Profile information
- `public_repos`, `followers`, `following`: Activity metrics
- `created_at`, `updated_at`: Timestamps

#### 2. **repositories**
Project repositories maintained by the users.

**Maps to GitHub API**: `/repos/{owner}/{repo}`

**Key Fields**:
- `github_id`: Unique GitHub repository ID
- `owner_id`: Reference to maintainer
- `stars`, `forks`, `watchers`, `open_issues`: Repository metrics
- `language`: Primary programming language

#### 3. **issues**
Issues created in repositories (includes bugs, features, questions).

**Maps to GitHub API**: `/repos/{owner}/{repo}/issues/{issue_number}`

**Key Fields**:
- `state`: 'open' or 'closed'
- `created_by`, `assigned_to`, `closed_by`: Maintainer references
- `labels`: JSONB array of label names
- `comments_count`: Number of comments

#### 4. **pull_requests**
Pull requests for code changes.

**Maps to GitHub API**: `/repos/{owner}/{repo}/pulls/{pull_number}`

**Key Fields**:
- `state`: 'open', 'closed', or 'merged'
- `merged_by`: Who merged the PR
- `commits_count`, `additions`, `deletions`, `changed_files`: Code change metrics
- `review_comments_count`: Number of review comments
- `draft`: Whether PR is in draft mode

#### 5. **pr_reviews**
Pull request reviews showing maintainer review activity.

**Maps to GitHub API**: `/repos/{owner}/{repo}/pulls/{pull_number}/reviews`

**Key Fields**:
- `state`: 'APPROVED', 'CHANGES_REQUESTED', 'COMMENTED', 'DISMISSED', 'PENDING'
- `reviewer_id`: Who performed the review
- `review_depth_score`: Custom score (0-10) indicating review thoroughness
- `lines_reviewed`: Estimated number of lines reviewed
- `submitted_at`: When review was submitted

**Special Note**: `review_depth_score` is a custom metric you'll calculate based on:
- Length of review body
- Number of inline comments
- Specificity of feedback
- Time spent (inferred from comment timestamps)

#### 6. **pr_review_comments**
Individual inline comments on PR diffs (shows mentorship activity).

**Maps to GitHub API**: `/repos/{owner}/{repo}/pulls/{pull_number}/comments`

**Key Fields**:
- `review_id`: Associated review
- `body`: Comment text (use this for sentiment analysis)
- `path`: File being commented on
- `position`, `line`: Location in diff
- `in_reply_to_id`: If replying to another comment (conversation thread)

#### 7. **issue_comments**
Comments on issues (shows community engagement).

**Maps to GitHub API**: `/repos/{owner}/{repo}/issues/{issue_number}/comments`

**Key Fields**:
- `body`: Comment text (use for sentiment analysis)
- `reactions`: JSONB object with reaction counts ("+1", "heart", "rocket", etc.)

#### 8. **issue_timeline_events**
Triage activities: labeling, assigning, closing issues.

**Maps to GitHub API**: `/repos/{owner}/{repo}/issues/{issue_number}/timeline`

**Key Fields**:
- `event_type`: 'labeled', 'unlabeled', 'assigned', 'unassigned', 'closed', 'reopened', etc.
- `actor_id`: Maintainer who performed the action
- `label_name`, `assignee_id`: Event-specific data

**Usage**: Track triage effectiveness by counting labeling, assignment, and closure events.

#### 9. **discussions**
GitHub Discussions for Q&A and community engagement.

**Maps to GitHub GraphQL API**: `discussion` type

**Key Fields**:
- `category`: 'Q&A', 'Ideas', 'Show and tell', etc.
- `is_answered`: Whether the discussion has been answered
- `answered_by`: Maintainer who provided the answer

#### 10. **discussion_comments**
Comments in discussions (shows mentorship and community support).

**Maps to GitHub GraphQL API**: `discussionComment` type

**Key Fields**:
- `is_answer`: Whether this comment was marked as the answer
- `parent_comment_id`: For threaded conversations
- `upvotes`: Community validation

#### 11. **commits**
Code commits (tracks documentation maintenance).

**Maps to GitHub API**: `/repos/{owner}/{repo}/commits/{sha}`

**Key Fields**:
- `is_docs_related`: Custom flag indicating documentation changes
- `additions`, `deletions`, `changed_files`: Code change metrics

#### 12. **sentiment_analysis**
AI sentiment analysis results for maintainer communications.

**Custom Table** (you'll populate this)

**Key Fields**:
- `content_type`: 'pr_review', 'issue_comment', 'discussion_comment'
- `content_id`: ID of the analyzed content
- `sentiment_score`: -1.0 (very negative) to 1.0 (very positive)
- `tone`: 'constructive', 'neutral', 'harsh', 'supportive'
- `text_analyzed`: The actual text that was analyzed

#### 13. **burnout_risk_scores**
Calculated burnout risk indicators.

**Custom Table** (you'll populate this)

**Key Fields**:
- `overall_risk_score`: 0-100 (higher = more risk)
- `response_time_score`: Degradation in response times
- `activity_level_score`: Decline in activity
- `sentiment_score`: Deterioration in sentiment
- `isolation_score`: Working alone vs. collaborative patterns
- `workload_score`: Hours/effort estimated
- `community_support_score`: Recognition and appreciation received

---

## GitHub API Mapping

### Available Data from GitHub API

#### 1. **Pull Request Reviews**
```
GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews
```
**Response includes**:
- `id`, `user`, `body`, `state`, `submitted_at`
- Review comments via: `/repos/{owner}/{repo}/pulls/{pull_number}/comments`

#### 2. **Pull Request Review Comments**
```
GET /repos/{owner}/{repo}/pulls/{pull_number}/comments
```
**Response includes**:
- `id`, `user`, `body`, `path`, `position`, `line`, `created_at`
- `in_reply_to_id` for conversation threads

#### 3. **Issue Comments**
```
GET /repos/{owner}/{repo}/issues/{issue_number}/comments
```
**Response includes**:
- `id`, `user`, `body`, `created_at`, `reactions`

#### 4. **Issue Timeline Events**
```
GET /repos/{owner}/{repo}/issues/{issue_number}/timeline
```
**Response includes**:
- `event`, `actor`, `created_at`
- Event-specific data (label, assignee, etc.)

#### 5. **Discussions** (GraphQL)
```graphql
query {
  repository(owner: "...", name: "...") {
    discussions(first: 100) {
      nodes {
        id, title, body, category, createdAt
        answer { author { login } }
        comments(first: 100) {
          nodes {
            author { login }
            body, createdAt, upvoteCount
          }
        }
      }
    }
  }
}
```

#### 6. **User Events**
```
GET /users/{username}/events
```
**Returns up to 300 events** (last 90 days):
- PR reviews, issue comments, commits, etc.

### NOT Available from GitHub API
- **Historical data beyond 90 days** for events
- **Sentiment analysis** (you must calculate)
- **Burnout indicators** (you must calculate)
- **Review depth scores** (you must calculate)
- **Mentorship metrics** (you must infer from comment patterns)

### Ecosyste.ms API
```
GET https://repos.ecosyste.ms/api/v1/hosts/github/repositories/{owner}/{repo}
```
**Provides**:
- Repository metadata
- Dependency information
- Package ecosystem data
- NOT useful for maintainer-specific invisible labor tracking

---

## Maintainer Personas

The dummy data includes 5 distinct maintainer personas with different patterns:

### 1. **Sarah Johnson** (@sarah_maintainer) - ID: 1
**Role**: Lead maintainer of awesome-framework

**Pattern**: **Burnout progression**
- **Week 1-2**: Highly active, supportive reviews, quick responses
- **Week 3**: Starting to show strain, slightly shorter responses
- **Week 4**: Burnt out - harsh reviews, slow responses, declining sentiment

**Metrics**:
- Initial sentiment: 0.85 (very positive)
- Final sentiment: 0.30 (slightly negative/frustrated)
- Burnout risk: 25 → 62 (high risk)
- Reviews with CHANGES_REQUESTED increasing
- Response time degrading

**Use Case**: Test burnout detection algorithms

### 2. **Alex Chen** (@alex_dev) - ID: 2
**Role**: Maintainer of data-processor

**Pattern**: **Healthy, consistent maintainer**
- Steady activity levels throughout
- Consistently constructive feedback
- Good work-life balance indicators
- Responsive but not overworked

**Metrics**:
- Stable sentiment: ~0.85
- Low burnout risk: ~20
- Balanced review patterns (APPROVED + CHANGES_REQUESTED)
- Regular response times

**Use Case**: Baseline for healthy maintainer metrics

### 3. **Morgan Lee** (@morgan_code) - ID: 3
**Role**: Maintainer of cli-toolbox, active contributor to others

**Pattern**: **Thriving maintainer & mentor**
- High quality, detailed reviews
- Active in discussions with helpful responses
- Offers to pair program and mentor
- Strong community engagement

**Metrics**:
- Excellent sentiment: ~0.90
- Very low burnout risk: ~15
- High mentorship indicators (long, detailed comments)
- Collaborative patterns (helps other maintainers)

**Use Case**: Example of excellent maintainer to highlight

### 4. **Jamie Rivera** (@jamie_oss) - ID: 4
**Role**: Growing contributor learning to maintain

**Pattern**: **Improving contributor becoming maintainer**
- Initially hesitant, asks many questions
- Receives mentorship from Sarah and Morgan
- Gradually takes on more responsibility
- Burnout risk decreases as confidence grows

**Metrics**:
- Improving sentiment: 0.75 → 0.86
- Decreasing burnout risk: 35 → 22
- Increasing review activity
- Learning patterns visible in comment threads

**Use Case**: Track mentorship success and contributor growth

### 5. **Riley Taylor** (@riley_contrib) - ID: 5
**Role**: Junior contributor to multiple projects

**Pattern**: **Enthusiastic but inexperienced**
- Very positive, eager to help
- Makes rookie mistakes that require review
- Receives extensive mentorship
- Slowly improving code quality

**Metrics**:
- Very positive sentiment: ~0.90
- Moderate burnout risk: ~35 (from overcommitment)
- High activity but needs guidance
- Receives detailed review comments (mentorship)

**Use Case**: Track mentee progress and mentorship effectiveness

---

## Data Patterns & Scenarios

### Scenario 1: Memory Leak Bug (Issue #1, PR #100)
**Pattern**: Quick critical bug fix with good triage

**Timeline**:
1. Riley reports issue with details (15 Sep)
2. Sarah quickly triages: labels (bug, high-priority), assigns self
3. Sarah investigates and reproduces
4. Riley opens PR with fix (16 Sep)
5. Sarah reviews with mentorship comments
6. PR merged quickly (20 Sep)
7. Issue closed with positive recognition

**Invisible Labor**:
- Triage: 5 timeline events
- Mentorship: 4 detailed review comments
- Community engagement: 8 issue comments
- Quick turnaround: 5 days

### Scenario 2: Security Vulnerability (Issue #4, PR #103)
**Pattern**: Urgent security response

**Timeline**:
1. Morgan reports security issue (25 Sep 16:00)
2. Sarah immediately labels (security, critical)
3. Sarah creates patch within 2 hours
4. Morgan reviews urgently
5. PR merged same day
6. Security advisory published
7. Community notified

**Invisible Labor**:
- Urgent triage: Immediate response
- Security handling: Coordinated disclosure
- Fast review cycle: Within hours
- Crisis management: Multiple updates

### Scenario 3: Feature Request with Mentorship (Issue #2, PR #101)
**Pattern**: Mentorship of new contributor

**Timeline**:
1. Jamie requests async middleware feature (18 Sep)
2. Sarah offers to mentor Jamie through implementation
3. Sarah provides detailed guidance (multiple comments)
4. Jamie asks clarifying questions
5. PR created with Sarah's guidance (19 Sep)
6. Multiple review cycles with constructive feedback
7. PR still open (learning in progress)

**Invisible Labor**:
- Mentorship: 11+ detailed guidance comments
- Code review: Multiple rounds with detailed feedback
- Architecture guidance: Explaining design patterns
- Encouragement: Positive reinforcement throughout

### Scenario 4: Performance Regression (Issue #5, PR #105)
**Pattern**: Burnout indicators during crisis

**Timeline**:
1. Alex reports performance issue (28 Sep)
2. Sarah's initial response is curt: "Need more details"
3. Sarah can't reproduce: "Can't reproduce. Need your configuration"
4. Morgan steps in to help investigate (29 Sep)
5. Morgan identifies root cause and fixes
6. Sarah thanks Morgan for covering

**Invisible Labor**:
- Morgan covering for burnt-out maintainer
- Collaborative problem-solving
- Community stepping up when leader is strained

### Scenario 5: Plugin System Discussion (Discussion #2)
**Pattern**: Architectural collaboration and planning

**Timeline**:
1. Morgan proposes plugin system (18 Sep)
2. Sarah asks thoughtful architecture questions
3. Community discusses various approaches
4. References to other projects (VSCode)
5. Offer to schedule video call for detailed design
6. Plans to create formal design document

**Invisible Labor**:
- Architecture planning: Deep technical discussions
- Research: Looking at other solutions
- Community building: Collaborative design process
- Documentation planning: Formal proposal creation

---

## Testing Your Dashboard

### Step 1: Load the Data
```bash
# Connect to your Neon Postgres database
psql 'postgresql://neondb_owner:npg_pNUL5s3VXolm@ep-dawn-firefly-a1vo09kv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# Load the dummy data
\i /path/to/maintainer_dashboard_dummy_data.sql
```

### Step 2: Verify Data Load
```sql
-- Check record counts
SELECT 'maintainers' as table_name, COUNT(*) FROM maintainers
UNION ALL
SELECT 'repositories', COUNT(*) FROM repositories
UNION ALL
SELECT 'issues', COUNT(*) FROM issues
UNION ALL
SELECT 'pull_requests', COUNT(*) FROM pull_requests
UNION ALL
SELECT 'pr_reviews', COUNT(*) FROM pr_reviews
UNION ALL
SELECT 'pr_review_comments', COUNT(*) FROM pr_review_comments
UNION ALL
SELECT 'issue_comments', COUNT(*) FROM issue_comments
UNION ALL
SELECT 'sentiment_analysis', COUNT(*) FROM sentiment_analysis
UNION ALL
SELECT 'burnout_risk_scores', COUNT(*) FROM burnout_risk_scores;

-- Expected counts:
-- maintainers: 5
-- repositories: 3
-- issues: 20
-- pull_requests: 23
-- pr_reviews: 60
-- pr_review_comments: 28
-- issue_comments: 68
-- issue_timeline_events: 63
-- discussions: 4
-- discussion_comments: 30
-- commits: 10
-- sentiment_analysis: 20
-- burnout_risk_scores: 20
```

### Step 3: Test Invisible Labor Scoring

#### Review Activity (30% weight)
```sql
SELECT 
    m.username,
    COUNT(DISTINCT pr.id) as total_reviews,
    AVG(pr.review_depth_score) as avg_depth_score,
    COUNT(CASE WHEN pr.state = 'CHANGES_REQUESTED' THEN 1 END) as changes_requested,
    COUNT(CASE WHEN pr.state = 'APPROVED' THEN 1 END) as approved,
    COUNT(DISTINCT prc.id) as inline_comments
FROM maintainers m
LEFT JOIN pr_reviews pr ON pr.reviewer_id = m.id
LEFT JOIN pr_review_comments prc ON prc.review_id = pr.id
GROUP BY m.id, m.username
ORDER BY total_reviews DESC;

-- Expected: Sarah (18), Alex (10), Morgan (16), Jamie (5), Riley (0)
```

#### Mentorship Score (25% weight)
```sql
SELECT 
    m.username,
    COUNT(DISTINCT prc.id) as review_comments,
    AVG(LENGTH(prc.body)) as avg_comment_length,
    COUNT(DISTINCT CASE 
        WHEN LENGTH(prc.body) > 200 THEN prc.id 
    END) as detailed_guidance_comments,
    COUNT(DISTINCT prc.in_reply_to_id) as conversation_threads
FROM maintainers m
LEFT JOIN pr_review_comments prc ON prc.commenter_id = m.id
GROUP BY m.id, m.username
ORDER BY detailed_guidance_comments DESC;

-- Expected: Sarah leads with detailed mentorship
-- Morgan has high-quality detailed comments
```

#### Triage Effectiveness (20% weight)
```sql
SELECT 
    m.username,
    COUNT(DISTINCT CASE WHEN ite.event_type = 'labeled' THEN ite.id END) as labels_added,
    COUNT(DISTINCT CASE WHEN ite.event_type = 'assigned' THEN ite.id END) as issues_assigned,
    COUNT(DISTINCT CASE WHEN ite.event_type = 'closed' THEN ite.id END) as issues_closed,
    COUNT(DISTINCT ite.issue_id) as total_issues_triaged
FROM maintainers m
LEFT JOIN issue_timeline_events ite ON ite.actor_id = m.id
GROUP BY m.id, m.username
ORDER BY total_issues_triaged DESC;

-- Expected: Sarah dominates triage for awesome-framework
-- Alex for data-processor, Morgan for cli-toolbox
```

#### Community Engagement (15% weight)
```sql
SELECT 
    m.username,
    COUNT(DISTINCT ic.id) as issue_comments,
    COUNT(DISTINCT dc.id) as discussion_comments,
    COUNT(DISTINCT d.id) FILTER (WHERE d.answered_by = m.id) as discussions_answered,
    SUM(COALESCE((ic.reactions->>'heart')::int, 0)) as hearts_received
FROM maintainers m
LEFT JOIN issue_comments ic ON ic.commenter_id = m.id
LEFT JOIN discussion_comments dc ON dc.commenter_id = m.id
LEFT JOIN discussions d ON d.answered_by = m.id
GROUP BY m.id, m.username
ORDER BY issue_comments + discussion_comments DESC;

-- Expected: All maintainers active in community
-- Morgan and Sarah lead in engagement
```

#### Documentation Maintenance (10% weight)
```sql
SELECT 
    m.username,
    COUNT(DISTINCT c.id) FILTER (WHERE c.is_docs_related = TRUE) as doc_commits,
    SUM(CASE WHEN c.is_docs_related THEN c.additions ELSE 0 END) as doc_additions
FROM maintainers m
LEFT JOIN commits c ON c.author_id = m.id
GROUP BY m.id, m.username
ORDER BY doc_commits DESC;

-- Expected: Sarah leads documentation work
```

### Step 4: Test Sentiment Analysis

#### Overall Sentiment Trends
```sql
SELECT 
    m.username,
    DATE(sa.analysis_date) as date,
    AVG(sa.sentiment_score) as avg_sentiment,
    MODE() WITHIN GROUP (ORDER BY sa.tone) as dominant_tone,
    COUNT(*) as total_interactions
FROM maintainers m
JOIN sentiment_analysis sa ON sa.maintainer_id = m.id
GROUP BY m.id, m.username, DATE(sa.analysis_date)
ORDER BY m.username, date;

-- Expected: Sarah's sentiment declining over time
-- Others remain stable or improve
```

#### Harsh Feedback Detection
```sql
SELECT 
    m.username,
    sa.tone,
    sa.sentiment_score,
    sa.analysis_date,
    LEFT(sa.text_analyzed, 100) as preview
FROM maintainers m
JOIN sentiment_analysis sa ON sa.maintainer_id = m.id
WHERE sa.sentiment_score < 0.4
ORDER BY sa.analysis_date;

-- Expected: Sarah's harsh comments appear in late September/early October
```

### Step 5: Test Burnout Risk Detection

#### Burnout Risk Over Time
```sql
SELECT 
    m.username,
    brs.calculation_date,
    brs.overall_risk_score,
    brs.response_time_score,
    brs.activity_level_score,
    brs.sentiment_score,
    brs.isolation_score,
    brs.workload_score,
    brs.community_support_score
FROM maintainers m
JOIN burnout_risk_scores brs ON brs.maintainer_id = m.id
ORDER BY m.username, brs.calculation_date;

-- Expected:
-- Sarah: 25 → 32 → 48 → 62 (escalating burnout)
-- Alex: Stable around 20 (healthy)
-- Morgan: Stable around 13 (thriving)
-- Jamie: 35 → 22 (improving)
-- Riley: 42 → 33 (learning to balance)
```

#### High-Risk Maintainers
```sql
SELECT 
    m.username,
    m.name,
    brs.overall_risk_score,
    brs.sentiment_score as sentiment_health,
    brs.response_time_score as response_degradation,
    brs.workload_score as workload_level
FROM maintainers m
JOIN burnout_risk_scores brs ON brs.maintainer_id = m.id
WHERE brs.calculation_date = (
    SELECT MAX(calculation_date) FROM burnout_risk_scores
)
AND brs.overall_risk_score >= 50
ORDER BY brs.overall_risk_score DESC;

-- Expected: Sarah appears with 62 risk score
```

### Step 6: Test Shareable Contribution Profile

#### Generate Profile Summary
```sql
WITH review_stats AS (
    SELECT 
        reviewer_id,
        COUNT(*) as total_reviews,
        AVG(review_depth_score) as avg_review_depth,
        COUNT(CASE WHEN state = 'APPROVED' THEN 1 END) as approvals,
        COUNT(CASE WHEN state = 'CHANGES_REQUESTED' THEN 1 END) as change_requests
    FROM pr_reviews
    WHERE submitted_at >= NOW() - INTERVAL '30 days'
    GROUP BY reviewer_id
),
comment_stats AS (
    SELECT 
        commenter_id,
        COUNT(DISTINCT ic.id) as issue_comments,
        COUNT(DISTINCT dc.id) as discussion_comments
    FROM issue_comments ic
    FULL OUTER JOIN discussion_comments dc ON ic.commenter_id = dc.commenter_id
    GROUP BY commenter_id
),
triage_stats AS (
    SELECT 
        actor_id,
        COUNT(*) as triage_actions,
        COUNT(DISTINCT issue_id) as issues_triaged
    FROM issue_timeline_events
    WHERE created_at >= NOW() - INTERVAL '30 days'
    GROUP BY actor_id
)
SELECT 
    m.username,
    m.name,
    m.company,
    m.location,
    COALESCE(rs.total_reviews, 0) as reviews_30d,
    ROUND(COALESCE(rs.avg_review_depth, 0), 2) as avg_review_quality,
    COALESCE(cs.issue_comments, 0) + COALESCE(cs.discussion_comments, 0) as community_engagement_30d,
    COALESCE(ts.triage_actions, 0) as triage_actions_30d,
    COALESCE(ts.issues_triaged, 0) as issues_triaged_30d
FROM maintainers m
LEFT JOIN review_stats rs ON rs.reviewer_id = m.id
LEFT JOIN comment_stats cs ON cs.commenter_id = m.id
LEFT JOIN triage_stats ts ON ts.actor_id = m.id
WHERE m.is_active = TRUE
ORDER BY reviews_30d DESC;
```

---

## Sample Queries

### Query 1: Top Reviewers by Depth
```sql
SELECT 
    m.username,
    COUNT(pr.id) as review_count,
    AVG(pr.review_depth_score) as avg_depth,
    SUM(pr.lines_reviewed) as total_lines_reviewed
FROM maintainers m
JOIN pr_reviews pr ON pr.reviewer_id = m.id
WHERE pr.submitted_at >= NOW() - INTERVAL '30 days'
GROUP BY m.id, m.username
ORDER BY avg_depth DESC, review_count DESC
LIMIT 10;
```

### Query 2: Mentorship Leaders
```sql
SELECT 
    mentor.username as mentor,
    mentee.username as mentee,
    COUNT(DISTINCT prc.id) as guidance_comments,
    AVG(LENGTH(prc.body)) as avg_comment_length
FROM pr_review_comments prc
JOIN maintainers mentor ON mentor.id = prc.commenter_id
JOIN pr_reviews pr ON pr.id = prc.review_id
JOIN pull_requests p ON p.id = pr.pull_request_id
JOIN maintainers mentee ON mentee.id = p.created_by
WHERE mentor.id != mentee.id
  AND LENGTH(prc.body) > 150  -- Substantial comments
GROUP BY mentor.id, mentor.username, mentee.id, mentee.username
HAVING COUNT(*) >= 3
ORDER BY guidance_comments DESC;
```

### Query 3: Burnout Alert System
```sql
SELECT 
    m.username,
    m.email,
    brs_current.overall_risk_score as current_risk,
    brs_prev.overall_risk_score as previous_risk,
    brs_current.overall_risk_score - brs_prev.overall_risk_score as risk_increase,
    CASE 
        WHEN brs_current.overall_risk_score >= 60 THEN 'CRITICAL'
        WHEN brs_current.overall_risk_score >= 40 THEN 'HIGH'
        WHEN brs_current.overall_risk_score >= 25 THEN 'MODERATE'
        ELSE 'LOW'
    END as risk_level
FROM maintainers m
JOIN burnout_risk_scores brs_current ON brs_current.maintainer_id = m.id
LEFT JOIN burnout_risk_scores brs_prev ON brs_prev.maintainer_id = m.id
WHERE brs_current.calculation_date = (
    SELECT MAX(calculation_date) FROM burnout_risk_scores
)
AND brs_prev.calculation_date = (
    SELECT MAX(calculation_date) 
    FROM burnout_risk_scores 
    WHERE calculation_date < (SELECT MAX(calculation_date) FROM burnout_risk_scores)
)
AND brs_current.overall_risk_score >= 40
ORDER BY brs_current.overall_risk_score DESC;
```

### Query 4: Sentiment Temperature Visualization
```sql
-- For each maintainer, get sentiment trend (for visualization)
WITH sentiment_buckets AS (
    SELECT 
        maintainer_id,
        DATE_TRUNC('week', analysis_date) as week,
        AVG(sentiment_score) as avg_sentiment,
        COUNT(*) as interaction_count,
        COUNT(CASE WHEN tone = 'harsh' THEN 1 END) as harsh_count,
        COUNT(CASE WHEN tone = 'supportive' THEN 1 END) as supportive_count
    FROM sentiment_analysis
    GROUP BY maintainer_id, DATE_TRUNC('week', analysis_date)
)
SELECT 
    m.username,
    sb.week,
    ROUND(sb.avg_sentiment::numeric, 3) as sentiment_score,
    sb.interaction_count,
    sb.harsh_count,
    sb.supportive_count,
    ROUND((sb.harsh_count::numeric / NULLIF(sb.interaction_count, 0)) * 100, 1) as harsh_percentage,
    CASE 
        WHEN sb.avg_sentiment >= 0.7 THEN '🟢 Positive'
        WHEN sb.avg_sentiment >= 0.4 THEN '🟡 Neutral'
        ELSE '🔴 Negative'
    END as sentiment_indicator
FROM maintainers m
JOIN sentiment_buckets sb ON sb.maintainer_id = m.id
ORDER BY m.username, sb.week;
```

### Query 5: Contribution CV Generator
```sql
-- Generate a shareable contribution CV
WITH date_range AS (
    SELECT 
        NOW() - INTERVAL '90 days' as start_date,
        NOW() as end_date
),
review_metrics AS (
    SELECT 
        reviewer_id,
        COUNT(*) as total_reviews,
        AVG(review_depth_score) as avg_quality,
        SUM(lines_reviewed) as lines_reviewed,
        COUNT(CASE WHEN state = 'APPROVED' THEN 1 END) as approvals,
        COUNT(CASE WHEN state = 'CHANGES_REQUESTED' THEN 1 END) as change_requests,
        COUNT(CASE WHEN state = 'COMMENTED' THEN 1 END) as comments_only
    FROM pr_reviews, date_range
    WHERE submitted_at BETWEEN start_date AND end_date
    GROUP BY reviewer_id
),
mentorship_metrics AS (
    SELECT 
        prc.commenter_id,
        COUNT(DISTINCT prc.id) as mentorship_comments,
        COUNT(DISTINCT prc.in_reply_to_id) FILTER (WHERE prc.in_reply_to_id IS NOT NULL) as replied_comments,
        AVG(LENGTH(prc.body)) as avg_guidance_length
    FROM pr_review_comments prc, date_range
    WHERE prc.created_at BETWEEN start_date AND end_date
      AND LENGTH(prc.body) > 100
    GROUP BY prc.commenter_id
),
triage_metrics AS (
    SELECT 
        actor_id,
        COUNT(*) as triage_actions,
        COUNT(DISTINCT issue_id) as issues_managed,
        COUNT(CASE WHEN event_type = 'labeled' THEN 1 END) as labels_added,
        COUNT(CASE WHEN event_type = 'assigned' THEN 1 END) as assignments_made,
        COUNT(CASE WHEN event_type = 'closed' THEN 1 END) as issues_closed
    FROM issue_timeline_events, date_range
    WHERE created_at BETWEEN start_date AND end_date
    GROUP BY actor_id
),
engagement_metrics AS (
    SELECT 
        ic.commenter_id,
        COUNT(DISTINCT ic.id) as issue_comments,
        SUM((ic.reactions->>'heart')::int) as hearts_received,
        SUM((ic.reactions->>'+1')::int) as thumbs_up_received
    FROM issue_comments ic, date_range
    WHERE ic.created_at BETWEEN start_date AND end_date
    GROUP BY ic.commenter_id
),
docs_metrics AS (
    SELECT 
        author_id,
        COUNT(*) FILTER (WHERE is_docs_related = TRUE) as doc_commits,
        SUM(additions) FILTER (WHERE is_docs_related = TRUE) as doc_lines_added
    FROM commits, date_range
    WHERE created_at BETWEEN start_date AND end_date
    GROUP BY author_id
)
SELECT 
    m.username,
    m.name,
    m.company,
    m.location,
    m.bio,
    -- Review Activity
    COALESCE(rm.total_reviews, 0) as reviews,
    ROUND(COALESCE(rm.avg_quality, 0), 2) as review_quality_score,
    COALESCE(rm.lines_reviewed, 0) as lines_reviewed,
    -- Mentorship
    COALESCE(mm.mentorship_comments, 0) as mentorship_interactions,
    ROUND(COALESCE(mm.avg_guidance_length, 0), 0) as avg_guidance_depth,
    -- Triage
    COALESCE(tm.triage_actions, 0) as triage_actions,
    COALESCE(tm.issues_managed, 0) as issues_triaged,
    COALESCE(tm.issues_closed, 0) as issues_resolved,
    -- Community
    COALESCE(em.issue_comments, 0) as community_responses,
    COALESCE(em.hearts_received, 0) as appreciation_hearts,
    -- Documentation
    COALESCE(dm.doc_commits, 0) as documentation_commits,
    COALESCE(dm.doc_lines_added, 0) as documentation_lines,
    -- Overall Score (weighted)
    ROUND(
        (COALESCE(rm.total_reviews, 0) * 0.30) +
        (COALESCE(mm.mentorship_comments, 0) * 0.25) +
        (COALESCE(tm.triage_actions, 0) * 0.20) +
        (COALESCE(em.issue_comments, 0) * 0.15) +
        (COALESCE(dm.doc_commits, 0) * 0.10),
        2
    ) as invisible_labor_score
FROM maintainers m
LEFT JOIN review_metrics rm ON rm.reviewer_id = m.id
LEFT JOIN mentorship_metrics mm ON mm.commenter_id = m.id
LEFT JOIN triage_metrics tm ON tm.actor_id = m.id
LEFT JOIN engagement_metrics em ON em.commenter_id = m.id
LEFT JOIN docs_metrics dm ON dm.author_id = m.id
WHERE m.is_active = TRUE
ORDER BY invisible_labor_score DESC;
```

---

## Next Steps

1. **Load the data** into your PostgreSQL database
2. **Run verification queries** to ensure data loaded correctly
3. **Test each scoring component**:
   - Review activity scoring
   - Mentorship metrics
   - Triage effectiveness
   - Community engagement
   - Documentation maintenance
4. **Test sentiment analysis pipeline** using the provided text
5. **Test burnout detection** using the progression data
6. **Build visualizations** using the sample queries
7. **Generate shareable profiles** using the CV query

Once everything works with dummy data, you can:
1. Connect to real GitHub API
2. Fetch actual data using the same structure
3. Process and store in the same tables
4. Run the same queries and algorithms

Good luck with your hackathon! 🚀
