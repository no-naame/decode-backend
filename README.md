# Maintainer's Dashboard - Backend API

A modular FastAPI backend for analyzing and supporting open source maintainers.

## 🎯 Project Overview

This dashboard helps open source maintainers by providing:
- **Invisible Labor Scoring** - Track and quantify non-code contributions
- **Sentiment Analysis** - Understand community dynamics and stress levels
- **Burnout Risk Detection** - Monitor and prevent maintainer burnout
- **Shareable Contribution Profiles** - Showcase your full contribution story

## 🏗️ Architecture

```
decode-dkmc/
├── main.py                  # FastAPI application entry point
├── app/
│   ├── core/               # Core configuration
│   │   └── config.py       # Settings and environment variables
│   ├── api/                # API routes
│   │   └── v1/
│   │       └── router.py   # Main API router
│   ├── modules/            # Feature modules (work independently)
│   │   ├── invisible_labor_scoring/
│   │   ├── sentiment_analysis/
│   │   ├── burnout_risk_detection/
│   │   └── shareable_contribution_profile/
│   └── shared/             # Shared utilities
│       ├── database.py     # Database connection
│       ├── github_client.py # GitHub API client
│       ├── cache.py        # Caching service
│       ├── models.py       # Shared models
│       ├── exceptions.py   # Custom exceptions
│       └── utils.py        # Utility functions
├── requirements.txt        # Python dependencies
└── .env.example           # Environment variables template
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

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

## 👥 Team Collaboration

### Module Assignment

Each team member has a dedicated module to work on independently:

1. **Team Member 1: Invisible Labor Scoring System**
   - Directory: `app/modules/invisible_labor_scoring/`
   - Routes: `/api/v1/invisible-labor-scoring/*`

2. **Team Member 2: Sentiment Analysis Engine**
   - Directory: `app/modules/sentiment_analysis/`
   - Routes: `/api/v1/sentiment-analysis/*`

3. **Team Member 3: Burnout Risk Detection**
   - Directory: `app/modules/burnout_risk_detection/`
   - Routes: `/api/v1/burnout-risk-detection/*`

4. **Team Member 4: Shareable Contribution Profile**
   - Directory: `app/modules/shareable_contribution_profile/`
   - Routes: `/api/v1/shareable-contribution-profile/*`

### Working on Your Module

1. Navigate to your module directory
2. All your work stays within your module folder
3. Each module has:
   - `routes.py` - API endpoints
   - `schemas.py` - Request/response models
   - `service.py` - Business logic
   - `README.md` - Module documentation
   - Create additional files as needed (`models.py`, `utils.py`, etc.)

### Shared Resources

Use shared utilities in `app/shared/`:
- `github_client.py` - GitHub API client
- `database.py` - Database connection
- `cache.py` - Caching service
- `models.py` - Shared data models
- `utils.py` - Common utilities

### Avoiding Conflicts

✅ **Safe to modify:**
- Your module directory (`app/modules/your_module/`)
- `requirements.txt` (add your dependencies)

❌ **Avoid modifying:**
- Other team members' modules
- Core files unless coordinated
- `main.py` (unless adding global middleware)

## 📝 Development Workflow

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-module-name
   ```

3. **Make changes in your module**

4. **Test your changes**
   ```bash
   python main.py
   # Visit http://localhost:8000/api/v1/docs
   ```

5. **Commit and push**
   ```bash
   git add app/modules/your_module/
   git commit -m "feat(your-module): description"
   git push origin feature/your-module-name
   ```

6. **Create Pull Request**

## 🧪 Testing Your Module

```bash
# Access your module's API docs
http://localhost:8000/api/v1/docs

# Test endpoints using Swagger UI
# Or use curl:
curl -X POST http://localhost:8000/api/v1/your-module/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

## 📚 API Documentation

Once running, comprehensive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🔧 Adding Dependencies

Add module-specific dependencies to `requirements.txt`:

```txt
# Your Module Name
your-library==1.0.0
another-dependency==2.0.0
```

Then run:
```bash
pip install -r requirements.txt
```

## 🌐 Environment Variables

Required environment variables (see `.env.example`):
- `GITHUB_TOKEN` - GitHub personal access token
- `DATABASE_URL` - Database connection string
- `ALLOWED_ORIGINS` - CORS allowed origins

## 🤝 Contributing

1. Each team member works on their assigned module
2. Follow the existing code structure
3. Update module README with your changes
4. Test your endpoints before pushing
5. Create descriptive commit messages
6. Request code review from team

## 📖 Module-Specific Documentation

Each module has its own README with detailed implementation guidelines:
- [Invisible Labor Scoring](app/modules/invisible_labor_scoring/README.md)
- [Sentiment Analysis](app/modules/sentiment_analysis/README.md)
- [Burnout Risk Detection](app/modules/burnout_risk_detection/README.md)
- [Shareable Contribution Profile](app/modules/shareable_contribution_profile/README.md)

## 🐛 Troubleshooting

**Import errors:**
```bash
# Make sure you're in the project root and virtual environment is activated
python main.py
```

**Database errors:**
```bash
# Delete the database and restart
rm maintainers_dashboard.db
python main.py
```

**Port already in use:**
```bash
# Change port in main.py or kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

## 📄 License

[Add your license here]

## 👨‍💻 Team

- Team Member 1: Invisible Labor Scoring
- Team Member 2: Sentiment Analysis
- Team Member 3: Burnout Risk Detection
- Team Member 4: Shareable Contribution Profile
# decode-backend
# decode-backend
