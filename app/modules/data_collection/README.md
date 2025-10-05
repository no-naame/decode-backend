# Data Collection Module

This module fetches and stores all available GitHub data for repositories into your database.

## Features

- ✅ Fetches data from both GitHub REST API and GraphQL API
- ✅ Stores data for the last 30 days (configurable)
- ✅ Collects all data types needed for invisible labor tracking:
  - Repository information
  - Maintainers (contributors)
  - Issues and issue comments
  - Pull requests, reviews, and review comments
  - Issue timeline events (triage activity)
  - Discussions and discussion comments
  - Commits
- ✅ No calculations - just stores raw GitHub data
- ✅ Repository-specific data collection

## API Endpoints

### Collect Repository Data
```bash
POST /api/v1/data-collection/collect
```

**Request Body:**
```json
{
  "owner": "facebook",
  "repo": "react",
  "days": 30,
  "token": "optional_github_token"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully collected data for facebook/react",
  "stats": {
    "repository_id": 1,
    "maintainers": 25,
    "issues": 150,
    "pull_requests": 80,
    "pr_reviews": 120,
    "pr_review_comments": 340,
    "issue_comments": 580,
    "issue_timeline_events": 420,
    "discussions": 15,
    "discussion_comments": 60,
    "commits": 200,
    "errors": [],
    "collection_time": 45.2
  }
}
```

### List Repositories
```bash
GET /api/v1/data-collection/repositories
```

Returns all repositories stored in the database.

### Get Repository Stats
```bash
GET /api/v1/data-collection/repositories/{owner}/{repo}/stats
```

Returns detailed statistics for a specific repository.

### List Maintainers
```bash
GET /api/v1/data-collection/maintainers?repository_id=1
```

Returns all maintainers, optionally filtered by repository.

### Delete Repository Data
```bash
DELETE /api/v1/data-collection/repositories/{owner}/{repo}
```

Deletes all data for a repository from the database.

## Usage Example

### 1. Start the server
```bash
python main.py
```

### 2. Collect data for a repository
```bash
curl -X POST "http://localhost:8000/api/v1/data-collection/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "facebook",
    "repo": "react",
    "days": 30
  }'
```

### 3. View collected data
```bash
# List repositories
curl "http://localhost:8000/api/v1/data-collection/repositories"

# Get repository stats
curl "http://localhost:8000/api/v1/data-collection/repositories/facebook/react/stats"

# List maintainers
curl "http://localhost:8000/api/v1/data-collection/maintainers"
```

## Data Structure

The module stores data in the following tables:

### Core Tables
- `maintainers` - GitHub users who contribute
- `repositories` - Project repositories

### Activity Tables
- `issues` - Issues in repositories
- `pull_requests` - Pull requests
- `pr_reviews` - PR reviews by maintainers
- `pr_review_comments` - Inline comments on PRs
- `issue_comments` - Comments on issues
- `issue_timeline_events` - Triage activities (labeling, assigning, etc.)
- `discussions` - GitHub Discussions
- `discussion_comments` - Discussion comments
- `commits` - Code commits

### Analysis Tables (To be populated later)
- `sentiment_analysis` - Sentiment scores (calculated separately)
- `burnout_risk_scores` - Burnout risk indicators (calculated separately)

## What Data is Collected

### ✅ Available from GitHub (stored directly)
- User profiles (name, email, bio, company, location)
- Repository metadata (stars, forks, language)
- Issues (title, body, state, labels, assignees)
- Pull requests (commits, additions, deletions, changed files)
- PR reviews (state, body, reviewer)
- PR review comments (inline code comments)
- Issue comments (body, reactions)
- Timeline events (labeled, assigned, closed, etc.)
- Discussions (title, body, category, answer)
- Discussion comments (body, upvotes, is_answer)
- Commits (message, additions, deletions, author)

### ❌ Not Available (to be calculated later)
- Review depth scores
- Mentorship indicators
- Documentation flags
- Sentiment scores
- Burnout risk scores
- Invisible labor scores

## GitHub Token

You can provide a GitHub token in three ways:

1. **Environment variable** (recommended):
   ```bash
   export GITHUB_TOKEN="your_token_here"
   ```

2. **In .env file**:
   ```
   GITHUB_TOKEN=your_token_here
   ```

3. **In API request**:
   ```json
   {
     "owner": "facebook",
     "repo": "react",
     "token": "your_token_here"
   }
   ```

## Rate Limits

- GitHub API rate limit: 5,000 requests/hour (authenticated)
- GraphQL API: 5,000 points/hour
- The collector makes multiple API calls per repository
- Large repositories may take several minutes to collect

## Error Handling

The collector continues even if some requests fail and returns errors in the response:

```json
{
  "stats": {
    "errors": [
      "Error fetching discussions: 404 Not Found"
    ]
  }
}
```

## Next Steps

After collecting data, you can:

1. **Calculate sentiment scores** using the Sentiment Analysis module
2. **Calculate burnout risk** using the Burnout Risk Detection module
3. **Calculate invisible labor scores** using the Invisible Labor Scoring module
4. **Generate contribution profiles** using the Shareable Contribution Profile module

## Database Schema

See `app/shared/models.py` for the complete database schema.

All tables include:
- Primary keys and foreign keys for relationships
- Timestamps (created_at, updated_at, fetched_at)
- GitHub IDs for deduplication
- All available fields from GitHub API

## Development

To modify the data collection logic:

1. **Add new fields**: Edit `app/shared/models.py`
2. **Add new API calls**: Edit `app/shared/github_data_collector.py`
3. **Add new endpoints**: Edit `app/modules/data_collection/routes.py`

## Testing

Test with a small repository first:
```bash
curl -X POST "http://localhost:8000/api/v1/data-collection/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "your-username",
    "repo": "small-test-repo",
    "days": 7
  }'
```

