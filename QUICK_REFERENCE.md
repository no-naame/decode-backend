# ⚡ Quick Reference Card

**Keep this handy while developing!**

## 🚀 Start Server

```bash
./run.sh                    # Quick start (recommended)
# OR
python main.py              # Direct start
```

**Access:**
- API Docs: http://localhost:8000/api/v1/docs
- Health: http://localhost:8000/health

---

## 📁 File Locations

```bash
# Your module
app/modules/your_module_name/

# Shared utilities
app/shared/

# Configuration
app/core/config.py
.env

# Main app
main.py
```

---

## 👥 Module Paths

| Module | Path |
|--------|------|
| Invisible Labor | `app/modules/invisible_labor_scoring/` |
| Sentiment | `app/modules/sentiment_analysis/` |
| Burnout | `app/modules/burnout_risk_detection/` |
| Profile | `app/modules/shareable_contribution_profile/` |

---

## 🔧 Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Check what's running
lsof -ti:8000

# Kill port 8000
lsof -ti:8000 | xargs kill -9

# Activate venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

# Python compile check
python -m py_compile main.py
```

---

## 🛠️ Using Shared Utilities

### GitHub API
```python
from app.shared.github_client import GitHubClient

client = GitHubClient()
user = await client.get_user("username")
repos = await client.get_user_repos("username")
commits = await client.get_commits("owner", "repo")
prs = await client.get_pull_requests("owner", "repo")
issues = await client.get_issues("owner", "repo")
```

### Cache
```python
from app.shared.cache import cache_service

await cache_service.set("key", data, ttl=3600)
data = await cache_service.get("key")
await cache_service.delete("key")
```

### Database
```python
from app.shared.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

@router.get("/endpoint")
async def endpoint(db: Session = Depends(get_db)):
    # use db here
    pass
```

### Utilities
```python
from app.shared.utils import (
    parse_github_repo,
    calculate_date_range,
    generate_cache_key,
    format_percentage,
    truncate_text
)
```

---

## 🎯 Module Structure

```python
# routes.py
from fastapi import APIRouter
router = APIRouter()

@router.post("/endpoint")
async def my_endpoint(request: MyRequest):
    result = await service.process(request)
    return result

# schemas.py
from pydantic import BaseModel

class MyRequest(BaseModel):
    field: str

class MyResponse(BaseModel):
    result: str

# service.py
class MyService:
    async def process(self, request):
        # Your logic here
        return result
```

---

## 📝 Git Workflow

```bash
# Daily workflow
git pull origin main
git checkout -b feature/my-feature

# Work...

git add app/modules/your_module/
git commit -m "feat: description"
git push origin feature/my-feature
```

**Commit message format:**
- `feat: new feature`
- `fix: bug fix`
- `docs: documentation`
- `refactor: code refactor`

---

## 🧪 Testing

### Swagger UI (Easiest)
1. Go to http://localhost:8000/api/v1/docs
2. Find your endpoint
3. Click "Try it out"
4. Test!

### cURL
```bash
curl -X POST http://localhost:8000/api/v1/your-module/endpoint \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

### Python requests
```python
import requests
r = requests.post(
    "http://localhost:8000/api/v1/your-module/endpoint",
    json={"field": "value"}
)
print(r.json())
```

---

## 📦 Adding Dependencies

1. Edit `requirements.txt`:
```txt
# Your Module
your-library==1.0.0
```

2. Install:
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Edit `.env`:
```bash
GITHUB_TOKEN=ghp_your_token_here
DATABASE_URL=sqlite:///./maintainers_dashboard.db
```

Get GitHub token: https://github.com/settings/tokens

---

## 🐛 Common Issues

**Port in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Import errors:**
```bash
pip install -r requirements.txt
```

**Venv issues:**
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `GETTING_STARTED.md` | Quick start |
| `TEAM_SETUP.md` | Team guide |
| `PROJECT_STRUCTURE.md` | Architecture |
| `TEMPLATE_SUMMARY.md` | Share with team |
| `QUICK_REFERENCE.md` | This file! |

---

## ✅ Quick Checklist

Before pushing:
- [ ] Code works locally
- [ ] Tested in Swagger UI
- [ ] Only modified your module
- [ ] Added dependencies to requirements.txt
- [ ] Commit message is clear

---

## 🔗 Important URLs

**Running locally:**
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc
- Health: http://localhost:8000/health
- Root: http://localhost:8000

**Learning:**
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- GitHub API: https://docs.github.com/en/rest

---

## 🎯 Module-Specific Routes

**Invisible Labor Scoring:**
```
POST /api/v1/invisible-labor-scoring/calculate
GET  /api/v1/invisible-labor-scoring/metrics/{username}
```

**Sentiment Analysis:**
```
POST /api/v1/sentiment-analysis/analyze
GET  /api/v1/sentiment-analysis/trends/{repository}
POST /api/v1/sentiment-analysis/batch-analyze
```

**Burnout Risk:**
```
POST /api/v1/burnout-risk-detection/assess
GET  /api/v1/burnout-risk-detection/alerts/{username}
GET  /api/v1/burnout-risk-detection/history/{username}
POST /api/v1/burnout-risk-detection/subscribe-alerts
```

**Shareable Profile:**
```
POST /api/v1/shareable-contribution-profile/generate
GET  /api/v1/shareable-contribution-profile/{username}
PUT  /api/v1/shareable-contribution-profile/{username}
GET  /api/v1/shareable-contribution-profile/{username}/public
GET  /api/v1/shareable-contribution-profile/{username}/export/{format}
```

---

**🚀 Happy Coding!**

*Print this and keep it near your desk!*
