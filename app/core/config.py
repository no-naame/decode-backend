from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Maintainer's Dashboard API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:5500"
    ]

    # Database
    DATABASE_URL: str = "sqlite:///./maintainers_dashboard.db"

    # GitHub API (for future integration)
    GITHUB_TOKEN: str = ""
    
    # GitHub App Authentication
    GITHUB_APP_ID: Optional[str] = None
    GITHUB_APP_SLUG: Optional[str] = None  # Your GitHub App slug/name
    GITHUB_PRIVATE_KEY: Optional[str] = None
    GITHUB_INSTALLATION_ID: Optional[str] = None
    
    # Gemini API
    GEMINI_API_KEY: str = ""

    # Redis (for caching, if needed)
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
