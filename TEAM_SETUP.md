# Team Setup Guide

Quick reference for getting your development environment ready.

## 🎯 Module Assignments

### Team Member 1: Invisible Labor Scoring System
**Directory:** `app/modules/invisible_labor_scoring/`
**API Prefix:** `/api/v1/invisible-labor-scoring`

**Your Tasks:**
- Calculate invisible labor scores from GitHub activity
- Track code reviews, issue triaging, documentation, mentoring
- Build scoring algorithm
- Create analytics endpoints

### Team Member 2: Sentiment Analysis Engine
**Directory:** `app/modules/sentiment_analysis/`
**API Prefix:** `/api/v1/sentiment-analysis`

**Your Tasks:**
- Analyze sentiment from PR/issue comments
- Implement NLP-based sentiment detection
- Track sentiment trends over time
- Build batch analysis capabilities

### Team Member 3: Burnout Risk Detection
**Directory:** `app/modules/burnout_risk_detection/`
**API Prefix:** `/api/v1/burnout-risk-detection`

**Your Tasks:**
- Detect burnout risk patterns
- Analyze work hours and activity patterns
- Generate alerts for high-risk cases
- Build recommendation system

### Team Member 4: Shareable Contribution Profile
**Directory:** `app/modules/shareable_contribution_profile/`
**API Prefix:** `/api/v1/shareable-contribution-profile`

**Your Tasks:**
- Generate beautiful shareable profiles
- Aggregate data from other modules
- Export profiles (PDF, HTML, Markdown)
- Build public profile pages

## 🚀 Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone <repository-url>
cd decode-dkmc

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Run the server
python main.py

# 6. Open browser
open http://localhost:8000/api/v1/docs
```

## 📁 Your Module Structure

Your module directory contains:

```
your_module/
├── __init__.py          # Python package marker
├── routes.py            # API endpoints (start here!)
├── schemas.py           # Request/response models
├── service.py           # Business logic
└── README.md            # Your module docs
```

**You can add:**
- `models.py` - Database models
- `utils.py` - Helper functions
- `tests.py` - Unit tests
- Any other files you need!

## 🔨 Development Workflow

### 1. Start with routes.py
Define your API endpoints:
```python
@router.get("/your-endpoint")
async def your_function():
    result = await service.do_something()
    return result
```

### 2. Define schemas in schemas.py
Create request/response models:
```python
class YourRequest(BaseModel):
    field1: str
    field2: int
```

### 3. Implement logic in service.py
Write your business logic:
```python
async def do_something(self, request):
    # Your implementation here
    return result
```

### 4. Use shared utilities
```python
from app.shared.github_client import GitHubClient
from app.shared.database import get_db
from app.shared.cache import cache_service

# GitHub API
client = GitHubClient()
user = await client.get_user("username")

# Caching
await cache_service.set("key", data, ttl=3600)
data = await cache_service.get("key")
```

## 🧪 Testing Your Work

### Option 1: Swagger UI (Recommended)
1. Run `python main.py`
2. Open http://localhost:8000/api/v1/docs
3. Find your module's endpoints
4. Click "Try it out" and test!

### Option 2: curl
```bash
curl -X POST http://localhost:8000/api/v1/your-module/endpoint \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

### Option 3: Python requests
```python
import requests
response = requests.post(
    "http://localhost:8000/api/v1/your-module/endpoint",
    json={"field": "value"}
)
print(response.json())
```

## 📦 Adding Dependencies

1. Add to `requirements.txt`:
```txt
# Your Module Name
your-library==1.0.0
```

2. Install:
```bash
pip install -r requirements.txt
```

## 🔄 Git Workflow

```bash
# Daily workflow
git pull origin main
git checkout -b feature/my-feature

# Work on your module...

git add app/modules/your_module/
git commit -m "feat(your-module): what you did"
git push origin feature/my-feature

# Create Pull Request on GitHub
```

## 🆘 Common Issues

**Import errors:**
```bash
# Make sure you're in project root
cd decode-dkmc
python main.py
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Port 8000 in use:**
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
# Or change port in main.py
```

**Virtual environment issues:**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🎓 Learning Resources

### FastAPI
- [Official Docs](https://fastapi.tiangolo.com/)
- [Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Pydantic (Schemas)
- [Documentation](https://docs.pydantic.dev/)

### SQLAlchemy (Database)
- [Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)

## 💡 Pro Tips

1. **Start Simple**: Get a basic endpoint working first
2. **Use Shared Code**: Don't duplicate GitHub API calls
3. **Add Type Hints**: Makes debugging easier
4. **Test Often**: Use Swagger UI frequently
5. **Read Module README**: Has specific guidance for your module
6. **Ask Questions**: Use team chat/issues

## 📞 Getting Help

1. Check your module's README
2. Review shared utilities in `app/shared/`
3. Look at other modules for examples
4. Ask your team members
5. Check FastAPI documentation

## ✅ Checklist for First Day

- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Server runs successfully
- [ ] Swagger UI accessible
- [ ] Your module's endpoints visible
- [ ] First test endpoint working

## 🎉 You're Ready!

Navigate to your module directory and start coding:
```bash
cd app/modules/your_module/
code .  # Opens in VS Code
```

Happy coding! 🚀
