from fastapi import APIRouter
from app.maintainer_dashboard.routes import router as dashboard_router

api_router = APIRouter()

# Main unified dashboard endpoint
api_router.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)
