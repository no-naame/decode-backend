from fastapi import APIRouter
from app.modules.invisible_labor_scoring.routes import router as invisible_labor_router
from app.modules.sentiment_analysis.routes import router as sentiment_router
from app.modules.burnout_risk_detection.routes import router as burnout_router
from app.modules.shareable_contribution_profile.routes import router as profile_router

api_router = APIRouter()

# Include all module routers
api_router.include_router(
    invisible_labor_router,
    prefix="/invisible-labor-scoring",
    tags=["Invisible Labor Scoring System"]
)

api_router.include_router(
    sentiment_router,
    prefix="/sentiment-analysis",
    tags=["Sentiment Analysis Engine"]
)

api_router.include_router(
    burnout_router,
    prefix="/burnout-risk-detection",
    tags=["Burnout Risk Detection"]
)

api_router.include_router(
    profile_router,
    prefix="/shareable-contribution-profile",
    tags=["Shareable Contribution Profile"]
)
