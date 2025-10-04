# 🚀 Getting Started - Quick Reference

**Welcome to the Maintainer's Dashboard Backend!**

This is your quick-start guide to get up and running in 5 minutes.

## ⚡ Super Quick Start

```bash
# 1. Clone and enter directory
cd decode-dkmc

# 2. Run the quick start script
./run.sh

# 3. Open your browser
open http://localhost:8000/api/v1/docs
```

That's it! 🎉

## 📋 What You Get

After running the script, you'll have:
- ✅ FastAPI server running on port 8000
- ✅ Swagger UI for testing APIs
- ✅ 4 modular workspaces ready for development
- ✅ Shared utilities for GitHub, Database, Cache
- ✅ Zero merge conflicts architecture

## 🎯 Your Module Assignment

Find your module in the table below:

| Team Member | Module | Directory | API Prefix |
|-------------|--------|-----------|------------|
| **Member 1** | Invisible Labor Scoring | `app/modules/invisible_labor_scoring/` | `/api/v1/invisible-labor-scoring` |
| **Member 2** | Sentiment Analysis | `app/modules/sentiment_analysis/` | `/api/v1/sentiment-analysis` |
| **Member 3** | Burnout Risk Detection | `app/modules/burnout_risk_detection/` | `/api/v1/burnout-risk-detection` |
| **Member 4** | Shareable Profile | `app/modules/shareable_contribution_profile/` | `/api/v1/shareable-contribution-profile` |

## 🗺️ Your Workspace

Navigate to your module:
```bash
cd app/modules/your_module_name/
```

You'll find:
```
your_module/
├── routes.py      ← Define your API endpoints here
├── schemas.py     ← Define request/response models
├── service.py     ← Write your business logic here
└── README.md      ← Your module's documentation
```

## 🛠️ First Steps

### 1. Test the Template (1 min)
```bash
# Start the server
python main.py

# Visit Swagger UI
open http://localhost:8000/api/v1/docs

# You'll see all 4 modules with placeholder endpoints!
```

### 2. Modify Your Module (5 min)

Open your `service.py` and replace placeholder logic:

```python
# Example: app/modules/invisible_labor_scoring/service.py

async def calculate_score(self, request):
    # Replace this placeholder with your actual logic
    # TODO: Fetch data from GitHub
    # TODO: Calculate invisible labor score
    # TODO: Store in database

    return InvisibleLaborScoreResponse(...)
```

### 3. Add Your Dependencies (2 min)

Edit `requirements.txt`:
```txt
# Your Module: Invisible Labor Scoring
numpy==1.26.3
pandas==2.1.4
```

Install:
```bash
pip install -r requirements.txt
```

### 4. Use Shared Utilities

```python
# In your service.py
from app.shared.github_client import GitHubClient
from app.shared.cache import cache_service

# Fetch GitHub data
client = GitHubClient()
repos = await client.get_user_repos("username")

# Cache results
await cache_service.set("key", data, ttl=3600)
```

## 🧪 Testing Your Work

### Method 1: Swagger UI (Easiest!)
1. Go to http://localhost:8000/api/v1/docs
2. Find your endpoint
3. Click "Try it out"
4. Enter test data
5. Click "Execute"
6. See the response!

### Method 2: cURL
```bash
curl -X POST http://localhost:8000/api/v1/your-module/endpoint \
  -H "Content-Type: application/json" \
  -d '{"username": "test"}'
```

### Method 3: Python
```python
import requests
r = requests.post(
    "http://localhost:8000/api/v1/your-module/endpoint",
    json={"username": "test"}
)
print(r.json())
```

## 🔑 Environment Setup

Copy and edit environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your GitHub token:
```bash
GITHUB_TOKEN=ghp_your_token_here
```

Get a GitHub token at: https://github.com/settings/tokens

## 📚 Documentation Guide

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **README.md** | Project overview | First read |
| **TEAM_SETUP.md** | Team onboarding | Before starting |
| **GETTING_STARTED.md** | Quick start (this file) | Start here! |
| **PROJECT_STRUCTURE.md** | Architecture details | Reference |
| **Module README** | Module-specific guide | When working on module |

## 🎓 Learning Path

### Day 1: Setup & Explore
- [ ] Clone repository
- [ ] Run the application
- [ ] Explore Swagger UI
- [ ] Test placeholder endpoints
- [ ] Read your module's README

### Day 2: First Feature
- [ ] Modify `service.py`
- [ ] Add custom logic
- [ ] Test with Swagger UI
- [ ] Use GitHub API client

### Day 3: Advanced Features
- [ ] Add database models
- [ ] Implement caching
- [ ] Create additional endpoints
- [ ] Write helper utilities

### Week 1: Integration
- [ ] Integrate with other modules (if needed)
- [ ] Add error handling
- [ ] Write tests
- [ ] Document your API

## 🔄 Daily Workflow

```bash
# Morning
git pull origin main              # Get latest changes
git checkout -b feature/my-work   # Create feature branch

# Development
# ... work on your module ...
python main.py                    # Test locally

# Evening
git add app/modules/your_module/  # Stage your changes
git commit -m "feat: what you did"
git push origin feature/my-work   # Push to remote
# Create Pull Request on GitHub
```

## 🐛 Common Issues & Fixes

### Server won't start
```bash
# Check if port is in use
lsof -ti:8000 | xargs kill -9

# Reinstall dependencies
pip install -r requirements.txt
```

### Import errors
```bash
# Make sure you're in the project root
cd decode-dkmc
python main.py
```

### Virtual environment issues
```bash
# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 💡 Pro Tips

1. **Keep it modular**: Don't modify other modules
2. **Use shared code**: GitHub client, cache, utils are ready
3. **Test frequently**: Swagger UI is your friend
4. **Git early, git often**: Small commits are better
5. **Read the READMEs**: Each module has specific guidance

## 📞 Help & Resources

### Quick Links
- **API Docs**: http://localhost:8000/api/v1/docs
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **GitHub API**: https://docs.github.com/en/rest

### File Locations
- **Your Module**: `app/modules/your_module_name/`
- **Shared Utils**: `app/shared/`
- **Config**: `app/core/config.py`
- **Main App**: `main.py`

### Important Commands
```bash
python main.py              # Run server
pip install -r requirements.txt   # Install deps
git status                  # Check git status
./run.sh                    # Quick start
```

## ✅ Checklist

Before you start coding:
- [ ] Server runs successfully
- [ ] Swagger UI accessible at /api/v1/docs
- [ ] You can see your module's endpoints
- [ ] You've read your module's README
- [ ] You have a GitHub token in .env
- [ ] Virtual environment activated

## 🎉 You're Ready!

Start coding in your module:
```bash
cd app/modules/your_module_name/
# Edit routes.py, schemas.py, service.py
# Test at http://localhost:8000/api/v1/docs
```

**Happy coding!** 🚀

---

*Need help? Check the other docs or ask your team!*
