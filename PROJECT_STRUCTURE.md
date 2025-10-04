# Project Structure Overview

## 📊 Visual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│                         (main.py)                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                ┌───────────┴────────────┐
                │   API Router (v1)      │
                │  /api/v1/...           │
                └───────────┬────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Module 1    │   │   Module 2    │   │   Module 3    │
│               │   │               │   │               │
│  Invisible    │   │  Sentiment    │   │   Burnout     │
│    Labor      │   │   Analysis    │   │     Risk      │
│   Scoring     │   │    Engine     │   │  Detection    │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        │    ┌──────────────┼──────────┐       │
        │    │              │          │       │
        ▼    ▼              ▼          ▼       ▼
    ┌────────────────────────────────────────────┐
    │         Shared Resources Layer             │
    ├────────────────────────────────────────────┤
    │ • GitHub API Client                        │
    │ • Database Connection                      │
    │ • Cache Service                            │
    │ • Common Models                            │
    │ • Utility Functions                        │
    └────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌──────────┐      ┌──────────┐        ┌──────────┐
  │ Database │      │  GitHub  │        │  Cache   │
  │ (SQLite) │      │   API    │        │ (Memory) │
  └──────────┘      └──────────┘        └──────────┘

┌───────────────────────────────────────────────────────────────┐
│                      Module 4                                  │
│           Shareable Contribution Profile                       │
│                                                                │
│  Aggregates data from Modules 1-3 to create                   │
│  beautiful shareable profiles                                  │
└───────────────────────────────────────────────────────────────┘
```

## 🗂️ File Structure

```
decode-dkmc/
│
├── 🚀 main.py                          # Application entry point
│
├── 📁 app/
│   ├── core/                           # Core configuration
│   │   └── config.py                   # Environment settings
│   │
│   ├── api/                            # API layer
│   │   └── v1/
│   │       └── router.py               # Routes aggregator
│   │
│   ├── modules/                        # Feature modules (TEAM WORKSPACES)
│   │   │
│   │   ├── invisible_labor_scoring/    # 👤 Team Member 1
│   │   │   ├── routes.py               # API endpoints
│   │   │   ├── schemas.py              # Data models
│   │   │   ├── service.py              # Business logic
│   │   │   └── README.md               # Module docs
│   │   │
│   │   ├── sentiment_analysis/         # 👤 Team Member 2
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── README.md
│   │   │
│   │   ├── burnout_risk_detection/     # 👤 Team Member 3
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── README.md
│   │   │
│   │   └── shareable_contribution_profile/  # 👤 Team Member 4
│   │       ├── routes.py
│   │       ├── schemas.py
│   │       ├── service.py
│   │       └── README.md
│   │
│   └── shared/                         # Shared utilities (ALL TEAM)
│       ├── database.py                 # DB connection & ORM
│       ├── github_client.py            # GitHub API wrapper
│       ├── cache.py                    # Caching layer
│       ├── models.py                   # Common models
│       ├── exceptions.py               # Custom exceptions
│       └── utils.py                    # Helper functions
│
├── 📝 requirements.txt                 # Python dependencies
├── 🔐 .env.example                     # Environment template
├── 🚫 .gitignore                       # Git ignore rules
├── 📖 README.md                        # Project documentation
├── 👥 TEAM_SETUP.md                    # Team onboarding guide
├── 📊 PROJECT_STRUCTURE.md             # This file
└── 🏃 run.sh                           # Quick start script
```

## 🔄 Request Flow

```
1. HTTP Request
   ↓
2. FastAPI (main.py)
   ↓
3. CORS Middleware
   ↓
4. API Router (/api/v1)
   ↓
5. Module Router (e.g., /invisible-labor-scoring)
   ↓
6. Route Handler (routes.py)
   ↓
7. Service Layer (service.py)
   ↓
8. Shared Resources (GitHub API, Database, Cache)
   ↓
9. Response (Pydantic Schema)
   ↓
10. JSON Response to Client
```

## 🎯 Module Independence

Each module is completely independent:

```
┌─────────────────────────────────────┐
│  Module: invisible_labor_scoring    │
├─────────────────────────────────────┤
│ ✅ Own routes.py                     │
│ ✅ Own schemas.py                    │
│ ✅ Own service.py                    │
│ ✅ Own business logic                │
│ ✅ Can add own files (models, utils)│
│ ✅ Separate API prefix               │
│ ✅ No conflicts with other modules   │
└─────────────────────────────────────┘
```

## 🔗 Shared Resources Usage

All modules can use shared resources:

```python
# In any module's service.py:

from app.shared.github_client import GitHubClient
from app.shared.cache import cache_service
from app.shared.database import get_db
from app.shared.utils import parse_github_repo

# Use GitHub API
client = GitHubClient()
user_data = await client.get_user("username")

# Use caching
await cache_service.set("key", data)
cached = await cache_service.get("key")

# Use database
# (with FastAPI dependency injection)
```

## 📡 API Endpoints Map

```
GET  /                              → Root welcome message
GET  /health                        → Health check

# Invisible Labor Scoring (Module 1)
POST /api/v1/invisible-labor-scoring/calculate
GET  /api/v1/invisible-labor-scoring/metrics/{username}

# Sentiment Analysis (Module 2)
POST /api/v1/sentiment-analysis/analyze
GET  /api/v1/sentiment-analysis/trends/{repository}
POST /api/v1/sentiment-analysis/batch-analyze

# Burnout Risk Detection (Module 3)
POST /api/v1/burnout-risk-detection/assess
GET  /api/v1/burnout-risk-detection/alerts/{username}
GET  /api/v1/burnout-risk-detection/history/{username}
POST /api/v1/burnout-risk-detection/subscribe-alerts

# Shareable Contribution Profile (Module 4)
POST /api/v1/shareable-contribution-profile/generate
GET  /api/v1/shareable-contribution-profile/{username}
PUT  /api/v1/shareable-contribution-profile/{username}
GET  /api/v1/shareable-contribution-profile/{username}/public
GET  /api/v1/shareable-contribution-profile/{username}/export/{format}
```

## 🛠️ Technology Stack

```
┌─────────────────────────────────────┐
│       Application Layer             │
│  • FastAPI (Web Framework)          │
│  • Pydantic (Data Validation)       │
│  • Uvicorn (ASGI Server)            │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         Data Layer                  │
│  • SQLAlchemy (ORM)                 │
│  • SQLite/PostgreSQL (Database)     │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│      Integration Layer              │
│  • HTTPX (Async HTTP Client)        │
│  • GitHub API                       │
└─────────────────────────────────────┘
```

## 🚦 Development Zones

### 🟢 GREEN ZONE (Safe to modify)
- Your assigned module directory
- requirements.txt (add your dependencies)
- Your module's README.md

### 🟡 YELLOW ZONE (Coordinate with team)
- Shared utilities (app/shared/)
- Database models (if adding shared models)
- Core configuration (if needed)

### 🔴 RED ZONE (Avoid modifying)
- Other team members' modules
- main.py (unless necessary)
- API router (app/api/v1/router.py)

## 📈 Scalability Design

The modular architecture supports:

1. **Horizontal Scaling**: Each module can be split into microservices
2. **Independent Development**: No merge conflicts
3. **Easy Testing**: Test modules independently
4. **Flexible Deployment**: Deploy modules separately if needed
5. **Clear Ownership**: Each team member owns their module

## 🔄 Data Flow Example

```
User requests invisible labor score
↓
POST /api/v1/invisible-labor-scoring/calculate
↓
invisible_labor_scoring/routes.py
↓
invisible_labor_scoring/service.py
↓
shared/github_client.py (fetch GitHub data)
↓
shared/cache.py (cache results)
↓
shared/database.py (store results)
↓
Return InvisibleLaborScoreResponse
```

## 🎓 Next Steps

1. **Read**: README.md for overview
2. **Setup**: Follow TEAM_SETUP.md
3. **Develop**: Work in your module
4. **Test**: Use Swagger UI at /api/v1/docs
5. **Integrate**: Use shared resources
6. **Deploy**: Follow deployment guide (TBD)
