# Maintainer's Dashboard - Backend API

A comprehensive FastAPI backend for analyzing and supporting open source maintainers.

## 🎯 Project Overview

This dashboard provides a unified API endpoint that analyzes open source maintainers and delivers:
- **Invisible Labor Score (0-100)** - Quantify non-code contributions
- **Review Impact Score** - Measure code review quality and effectiveness
- **Community Engagement** - Track community building efforts
- **Burnout Risk Assessment** - Monitor and prevent maintainer burnout
- **Sentiment Analysis** - Understand community feedback patterns
- **Contribution Profile** - Comprehensive shareable profile with achievements

## 🏗️ Architecture

```
decode-dkmc/
├── main.py                     # FastAPI application entry point
├── app/
│   ├── core/                   # Core configuration
│   │   └── config.py           # Settings and environment variables
│   ├── api/                    # API routes
│   │   └── v1/
│   │       └── router.py       # Main API router
│   ├── maintainer_dashboard/   # Dashboard module
│   │   ├── routes.py           # API endpoint
│   │   ├── schemas.py          # Pydantic models
│   │   ├── service.py          # Business logic orchestration
│   │   ├── calculator.py       # Metric calculation engine
│   │   └── ai_insights.py      # Gemini AI integration
│   └── shared/                 # Shared utilities
│       ├── database.py         # Database connection
│       ├── github_client.py    # GitHub API client
│       ├── cache.py            # Caching service
│       ├── models.py           # Shared data models
│       ├── exceptions.py       # Custom exceptions
│       └── utils.py            # Utility functions
├── requirements.txt            # Python dependencies
├── DOCUMENTATION.md            # Detailed documentation
├── OPENAPI_SPEC.md             # OpenAPI specification
└── datawehave.md               # Available data sources
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd decode-dkmc
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

   Required variables:
   - `GITHUB_TOKEN` - GitHub personal access token (optional, for real GitHub API calls)
   - `GEMINI_API_KEY` - Google Gemini API key (optional, for AI insights)
   - `DATABASE_URL` - Database connection string
   - `ALLOWED_ORIGINS` - CORS allowed origins

5. **Run the application**
   ```bash
   python main.py
   # Or use the run script
   ./run.sh
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

## 📡 API Usage

### Main Endpoint

**GET** `/api/v1/dashboard/{username}`

Returns complete dashboard data for a GitHub user.

**Parameters:**
- `username` (path) - GitHub username
- `repository` (query, optional) - Filter by specific repository (format: "owner/repo")
- `days` (query, default=30) - Time window for analysis (7-365 days)

**Example:**
```bash
curl "http://localhost:8000/api/v1/dashboard/sarah_maintainer?days=30"
```

**Response includes:**
- Metrics (all scores, weekly activity, trends)
- Burnout assessment with AI recommendations
- Sentiment analysis with word frequency
- Community metrics
- Contribution profile with achievements & skills
- Alerts
- Recent activity timeline
- Repository health stats

## 🧮 Metric Calculations

All metrics use rigorous, documented formulas:

### Invisible Labor Score (0-100)
- Code Reviews (35%): Quality and depth of reviews
- Issue Triage (25%): Labeling, assignment, closure
- Mentorship (20%): Detailed explanations and guidance
- Community (15%): Discussions and support
- Documentation (5%): Docs commits and improvements

### Review Impact Score (0-100)
- Thoroughness (40%): Lines reviewed, comment depth
- Timeliness (30%): Response speed
- Helpfulness (30%): Approval ratio

### Burnout Risk (0-100)
- Workload (30%): Activities per day
- Irregular Hours (25%): Weekend/late-night work
- Sentiment Decline (25%): Mood tracking
- Response Pressure (20%): Activity density

## 🤖 AI Integration

Uses Google Gemini 2.0 Flash for:
- Burnout recovery recommendations
- Sentiment feedback analysis
- Impact summaries

**Anti-hallucination measures:**
- Low temperature (0.3) for factual responses
- Grounded prompts with specific numeric data
- Validation against actual data
- Fallback to safe defaults

## 🗄️ Data Sources

Currently uses mock data for testing. To integrate real GitHub API:

1. Set `GITHUB_TOKEN` in `.env`
2. Replace `_fetch_github_data()` in `service.py` with actual API calls
3. Use the `GitHubClient` in `app/shared/github_client.py`

**Available GitHub API endpoints:**
- User info, repositories, commits
- Pull requests, reviews, comments
- Issues, timeline events, labels
- Discussions (GraphQL)

## 🧪 Testing

```bash
# Start server
python main.py

# Test endpoint
curl "http://localhost:8000/api/v1/dashboard/sarah_maintainer?days=30"

# Or use Swagger UI
open http://localhost:8000/api/v1/docs
```

## 📚 Documentation

- [DOCUMENTATION.md](DOCUMENTATION.md) - Detailed feature documentation
- [OPENAPI_SPEC.md](OPENAPI_SPEC.md) - Complete API specification
- [datawehave.md](datawehave.md) - Available data sources from GitHub

## 🔧 Development

### Project Structure

- **Modular**: Dashboard logic separated into focused files
- **Typed**: Full Pydantic validation
- **Documented**: Every calculation formula explained
- **Tested**: Ready for real GitHub API integration

### Adding Features

1. Update `schemas.py` with new models
2. Add calculations to `calculator.py`
3. Update `service.py` to orchestrate
4. Extend AI insights in `ai_insights.py` if needed

## 🐛 Troubleshooting

**Import errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
python main.py
```

**Database errors:**
```bash
# Delete database and restart
rm maintainers_dashboard.db
python main.py
```

**Port already in use:**
```bash
# Change port in main.py or kill process
lsof -ti:8000 | xargs kill -9
```

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

Built with:
- FastAPI - Modern Python web framework
- Pydantic - Data validation
- SQLAlchemy - Database ORM
- Google Gemini - AI insights
- GitHub API - Data source
